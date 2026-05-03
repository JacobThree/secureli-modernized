# Graph Report - secureli-modernized  (2026-05-03)

## Corpus Check
- 104 files · ~33,673 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 956 nodes · 2430 edges · 16 communities detected
- Extraction: 42% EXTRACTED · 58% INFERRED · 0% AMBIGUOUS · INFERRED: 1417 edges (avg confidence: 0.65)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]

## God Nodes (most connected - your core abstractions)
1. `EchoAbstraction` - 83 edges
2. `PreCommitSettings` - 50 edges
3. `VersionControlRepoAbstraction` - 46 edges
4. `SecureliConfig` - 43 edges
5. `PreCommitAbstraction` - 41 edges
6. `Color` - 38 edges
7. `LogAction` - 36 edges
8. `Level` - 35 edges
9. `Action` - 34 edges
10. `HooksScannerService` - 34 edges

## Surprising Connections (you probably didn't know these)
- `SecureliRepository` --calls--> `settings_repository()`  [INFERRED]
  secureli/repositories/repo_settings.py → tests/repositories/test_settings_repository.py
- `ActionDependencies` --calls--> `action_deps()`  [INFERRED]
  secureli/actions/action.py → tests/actions/test_initializer_action.py
- `ActionDependencies` --calls--> `action_deps()`  [INFERRED]
  secureli/actions/action.py → tests/actions/test_scan_action.py
- `ActionDependencies` --calls--> `action_deps()`  [INFERRED]
  secureli/actions/action.py → tests/actions/test_update_action.py
- `ActionDependencies` --calls--> `action_deps()`  [INFERRED]
  secureli/actions/action.py → tests/actions/test_action.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.03
Nodes (85): Prints the provided message to the terminal in red and bold         :param messa, Encapsulates the Typer dependency for printing purposes, allows us to render stu, Print the provided info message to the terminal with the associated color and we, Prints the message to the terminal in blue and bold         :param message: The, Print the provided info message to the terminal with the associated color and we, Prints the provided message to the terminal in red and bold         :param messa, TyperEcho, InstallResult (+77 more)

### Community 1 - "Community 1"
Cohesion: 0.03
Nodes (97): Print the provided message to the terminal with the associated color and weight, Prompt the user for confirmation         :param message: The message to display, Prompts the user to enter a value         :param message: The message to display, ExecuteFailedError, InstallFailedError, InstallLanguageConfigError, Execute the configured hooks against the repository, either against your staged, Call's pre-commit's undocumented/internal functions to check for updates to repo (+89 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (74): ABC, EchoAbstraction, Encapsulates the printing purposes, allows us to render stuff to the screen., list_staged_files(), Abstracts common version control repository functions, VersionControlRepoAbstraction, Action, Action (+66 more)

### Community 3 - "Community 3"
Cohesion: 0.05
Nodes (65): Renders the epilog to display as part of the application help text., Arranges various properties needed to set up the application itself., SetupAction, test_that_initialize_repo_install_flow_displays_security_analysis_results(), test_publish_results_always(), test_publish_results_on_fail_and_action_not_successful(), test_publish_results_on_fail_and_action_successful(), test_that_secureli_yaml_settings_guards_against_missing_yaml_file() (+57 more)

### Community 4 - "Community 4"
Cohesion: 0.07
Nodes (51): PreCommitAbstraction, Returns the expected/non-deprecated path for .pre-commit-config.yaml.         If, Returns whether a pre-commit-config exists in a given folder path, Abstracts the configuring and execution of pre-commit., test_get_pre_commit_config_path_is_correct_returns_expected_values(), Scans the repo according to the repo's seCureLI config, LanguageSupportService, Creates a basic, serializable configuration out of the combined specified langua (+43 more)

### Community 5 - "Community 5"
Cohesion: 0.05
Nodes (40): action_deps(), mock_custom_scanners(), mock_hooks_scanner(), mock_pass_install_verification(), test_that_scan_checks_for_updates(), test_that_scan_only_checks_for_updates_periodically(), test_that_scan_repo_conducts_all_scans_and_merges_results(), test_that_scan_repo_continue_scan_if_upgrade_canceled() (+32 more)

### Community 6 - "Community 6"
Cohesion: 0.05
Nodes (40): LexerGuesser, PygmentsLexerGuesser, Pygments-implementation of LexerGuesser, Represents guessing the lexer for a given file., pygments_lexer_guesser(), test_that_pygments_lexer_guesser_guesses_lexer_with_pygments(), list_repo_files(), load_file() (+32 more)

### Community 7 - "Community 7"
Cohesion: 0.05
Nodes (37): Handles update operations, LogEntry, LogFailure, An extendable structure for log failures, A distinct entry in the log captured following actions like scan and init, Enables capturing secureli KPI log entries to a local file for future upload, Capture that a successful conclusion has been reached for an action         :par, Capture a failure against an action, with details         :param action: The act (+29 more)

### Community 8 - "Community 8"
Cohesion: 0.06
Nodes (36): Creates a new  pre-commit hook file in .git/hooks with the SeCureLI pre-commit h, test_that_pre_commit_install_creates_backup_file_when_already_exists(), test_that_pre_commit_install_creates_pre_commit_hook_for_secureli(), BadIgnoreBlockError, GitIgnoreService, Manages entries in a consuming repository's gitignore so that secureli doesn't, Creates a .gitignore, appends to an existing one, or updates the configuration, Create a .gitignore block of our ignore entries wrapped by a constant header and (+28 more)

### Community 9 - "Community 9"
Cohesion: 0.06
Nodes (32): ExecuteResult, Installs the hooks defined in pre-commit-config.yml.         :param folder_path:, Removes unused hook repos from the cache.  Pre-commit determines which flags are, The results of calling execute_hooks, test_that_pre_commit_remove_unused_hooks_properly_handles_failed_executions(), test_that_pre_commit_remove_unused_hookss_executes_successfully(), test_that_pre_commit_update_executes_successfully(), test_that_pre_commit_update_properly_handles_failed_executions() (+24 more)

### Community 10 - "Community 10"
Cohesion: 0.07
Nodes (27): build_action(), test_that_build_action_respects_color_choice(), action_deps(), initializer_action(), test_that_initialize_repo_does_not_load_config_when_resetting(), test_that_initialize_repo_logs_failure_when_failing_to_verify(), scan_action(), update_action() (+19 more)

### Community 11 - "Community 11"
Cohesion: 0.08
Nodes (23): mock_repo_files_value_error(), BinaryFileError, GitRepo, True if the file does not match on patterns within secureliignore or gitignore, True if the file's extension isn't ignored by secureli         :param file_path:, The loaded file was a binary and cannot be scanned., True if the file itself and any of its folders respective to the working, Confirms a provided path is a git repo, and if not raises a ValueError         : (+15 more)

### Community 12 - "Community 12"
Cohesion: 0.11
Nodes (21): LanguageConfigService, Load any config files for given language if they exist.         :param language:, Calculates a hash of the pre-commit file for the given language to be used as pa, Combine elements of our configuration for the specified language along with, Combine elements of our configuration for the specified language along with, language_config_service(), test_that_calculate_combined_configuration_adds_lint_config(), test_that_calculate_combined_configuration_ignores_lint_config() (+13 more)

### Community 13 - "Community 13"
Cohesion: 0.12
Nodes (13): test_that_container_loads(), CustomScanId, Scan ids of custom scans, Enum, VerifyConfigOutcome, ActionSource, LogStatus, Whether the entry represents a successful or failing entry (+5 more)

### Community 14 - "Community 14"
Cohesion: 0.67
Nodes (1): main()

### Community 15 - "Community 15"
Cohesion: 0.67
Nodes (1): Program

## Knowledge Gaps
- **37 isolated node(s):** `Save and retrieve the seCureLI configuration`, `Save the specified configuration to the .secureli folder         :param secureli`, `Load the seCureLI config from the expected configuration file path or return a n`, `Check secureli config and verify that it matches most current schema.`, `Update any older config version to match most current config.` (+32 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 14`** (3 nodes): `main()`, `main.go`, `Main.kt`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (3 nodes): `Program`, `.Main()`, `Program.cs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `EchoAbstraction` connect `Community 2` to `Community 0`, `Community 1`, `Community 4`, `Community 8`, `Community 9`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._
- **Why does `mock_open()` connect `Community 8` to `Community 1`, `Community 3`, `Community 4`, `Community 5`, `Community 6`, `Community 7`, `Community 9`, `Community 10`, `Community 11`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Why does `PreCommitAbstraction` connect `Community 4` to `Community 1`, `Community 2`, `Community 7`, `Community 8`, `Community 9`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Are the 73 inferred relationships involving `EchoAbstraction` (e.g. with `BuildAction` and `An action responsible for displaying the Securbuild ASCII art in the terminal du`) actually correct?**
  _`EchoAbstraction` has 73 INFERRED edges - model-reasoned connections that need verification._
- **Are the 47 inferred relationships involving `PreCommitSettings` (e.g. with `HooksScannerService` and `Scans the repo according to the repo's seCureLI config`) actually correct?**
  _`PreCommitSettings` has 47 INFERRED edges - model-reasoned connections that need verification._
- **Are the 43 inferred relationships involving `VersionControlRepoAbstraction` (e.g. with `Container` and `Arrange various dependencies and instruct the system on how to wire them up.`) actually correct?**
  _`VersionControlRepoAbstraction` has 43 INFERRED edges - model-reasoned connections that need verification._
- **Are the 42 inferred relationships involving `SecureliConfig` (e.g. with `VerifyOutcome` and `ActionSource`) actually correct?**
  _`SecureliConfig` has 42 INFERRED edges - model-reasoned connections that need verification._