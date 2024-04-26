//! Provides an solver implementation based on the [`rattler_libsolv_c`] crate.

use crate::{IntoRepoData, SolverRepoData};
use crate::{SolveError, SolverTask};
pub use input::cache_repodata;
use input::{add_repodata_records, add_solv_file, add_virtual_packages};
pub use libc_byte_slice::LibcByteSlice;
use output::get_required_packages;
use rattler_conda_types::RepoDataRecord;
use std::collections::HashMap;
use std::ffi::CString;
use std::mem::ManuallyDrop;
use wrapper::{
    flags::SolverFlag,
    pool::{Pool, Verbosity},
    repo::Repo,
    solve_goal::SolveGoal,
};

mod input;
mod libc_byte_slice;
mod output;
mod wrapper;

/// Represents the information required to load available packages into libsolv for a single channel
/// and platform combination
#[derive(Clone)]
pub struct RepoData<'a> {
    /// The actual records after parsing `repodata.json`
    pub records: Vec<&'a RepoDataRecord>,

    /// The in-memory .solv file built from the records (if available)
    pub solv_file: Option<&'a LibcByteSlice>,
}

impl<'a> FromIterator<&'a RepoDataRecord> for RepoData<'a> {
    fn from_iter<T: IntoIterator<Item = &'a RepoDataRecord>>(iter: T) -> Self {
        Self {
            records: Vec::from_iter(iter),
            solv_file: None,
        }
    }
}

impl<'a> RepoData<'a> {
    /// Constructs a new `LibsolvRsRepoData`
    #[deprecated(since = "0.6.0", note = "use From::from instead")]
    pub fn from_records(records: impl Into<Vec<&'a RepoDataRecord>>) -> Self {
        Self {
            records: records.into(),
            solv_file: None,
        }
    }
}

impl<'a> SolverRepoData<'a> for RepoData<'a> {}

/// Convenience method that converts a string reference to a `CString`, replacing NUL characters
/// with whitespace (`b' '`)
fn c_string<T: AsRef<str>>(str: T) -> CString {
    let bytes = str.as_ref().as_bytes();

    let mut vec = Vec::with_capacity(bytes.len() + 1);
    vec.extend_from_slice(bytes);

    for byte in &mut vec {
        if *byte == 0 {
            *byte = b' ';
        }
    }

    // Trailing 0
    vec.push(0);

    // Safe because the string does is guaranteed to have no NUL bytes other than the trailing one
    unsafe { CString::from_vec_with_nul_unchecked(vec) }
}

/// A [`Solver`] implemented using the `libsolv` library
#[derive(Default)]
pub struct Solver;

impl super::SolverImpl for Solver {
    type RepoData<'a> = RepoData<'a>;

    fn solve<
        'a,
        R: IntoRepoData<'a, Self::RepoData<'a>>,
        TAvailablePackagesIterator: IntoIterator<Item = R>,
    >(
        &mut self,
        task: SolverTask<TAvailablePackagesIterator>,
    ) -> Result<Vec<RepoDataRecord>, SolveError> {
        if task.timeout.is_some() {
            return Err(SolveError::UnsupportedOperations(vec![
                "timeout".to_string()
            ]));
        }

        // Construct a default libsolv pool
        let pool = Pool::default();

        // Setup proper logging for the pool
        pool.set_debug_callback(|msg, _flags| {
            tracing::event!(tracing::Level::DEBUG, "{}", msg.trim_end());
        });
        pool.set_debug_level(Verbosity::Low);

        // Add virtual packages
        let repo = Repo::new(&pool, "virtual_packages");
        add_virtual_packages(&pool, &repo, &task.virtual_packages);

        // Mark the virtual packages as installed.
        pool.set_installed(&repo);

        // Create repos for all channel + platform combinations
        let mut repo_mapping = HashMap::new();
        let mut all_repodata_records = Vec::new();
        for repodata in task.available_packages.into_iter().map(IntoRepoData::into) {
            if repodata.records.is_empty() {
                continue;
            }

            let channel_name = &repodata.records[0].channel;

            // We dont want to drop the Repo, its stored in the pool anyway.
            let repo = ManuallyDrop::new(Repo::new(&pool, channel_name));

            if let Some(solv_file) = repodata.solv_file {
                add_solv_file(&pool, &repo, solv_file);
            } else {
                add_repodata_records(&pool, &repo, repodata.records.iter().copied());
            }

            // Keep our own info about repodata_records
            repo_mapping.insert(repo.id(), repo_mapping.len());
            all_repodata_records.push(repodata.records);
        }

        // Create a special pool for records that are already installed or locked.
        let repo = Repo::new(&pool, "locked");
        let installed_solvables = add_repodata_records(&pool, &repo, &task.locked_packages);

        // Also add the installed records to the repodata
        repo_mapping.insert(repo.id(), repo_mapping.len());
        all_repodata_records.push(task.locked_packages.iter().collect());

        // Create a special pool for records that are pinned and cannot be changed.
        let repo = Repo::new(&pool, "pinned");
        let pinned_solvables = add_repodata_records(&pool, &repo, &task.pinned_packages);

        // Also add the installed records to the repodata
        repo_mapping.insert(repo.id(), repo_mapping.len());
        all_repodata_records.push(task.pinned_packages.iter().collect());

        // Create datastructures for solving
        pool.create_whatprovides();

        // Add matchspec to the queue
        let mut goal = SolveGoal::default();

        // Favor the currently installed packages
        for favor_solvable in installed_solvables {
            goal.favor(favor_solvable);
        }

        // Lock the currently pinned packages
        for locked_solvable in pinned_solvables {
            goal.lock(locked_solvable);
        }

        // Specify the matchspec requests
        for spec in task.specs {
            let id = pool.intern_matchspec(&spec);
            goal.install(id, false);
        }

        // Construct a solver and solve the problems in the queue
        let mut solver = pool.create_solver();
        solver.set_flag(SolverFlag::allow_uninstall(), true);
        solver.set_flag(SolverFlag::allow_downgrade(), true);

        let transaction = solver.solve(&mut goal).map_err(SolveError::Unsolvable)?;

        let required_records = get_required_packages(
            &pool,
            &repo_mapping,
            &transaction,
            all_repodata_records.as_slice(),
        )
        .map_err(|unsupported_operation_ids| {
            SolveError::UnsupportedOperations(
                unsupported_operation_ids
                    .into_iter()
                    .map(|id| format!("libsolv operation {id}"))
                    .collect(),
            )
        })?;

        Ok(required_records)
    }
}

#[cfg(test)]
mod test {
    use super::*;
    use rstest::rstest;

    #[rstest]
    #[case("", "")]
    #[case("a\0b\0c\0d\0", "a b c d ")]
    #[case("a b c d", "a b c d")]
    #[case("😒", "😒")]
    fn test_c_string(#[case] input: &str, #[case] expected_output: &str) {
        let output = c_string(input);
        assert_eq!(output.as_bytes(), expected_output.as_bytes());
    }
}
