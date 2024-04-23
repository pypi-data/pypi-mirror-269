# Copyright (c) 2024 Henix, Henix.fr
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test case metadata retrieval helpers"""

from typing import Any, Dict, Generator, List, Optional, Set
from collections import defaultdict

from opentf.commons.expressions import evaluate_bool
from opentf.toolkit.core import warning


########################################################################
# Constants

SUCCESS = 'SUCCESS'
FAILURE = 'FAILURE'
ERROR = 'ERROR'
SKIPPED = 'SKIPPED'
TOTAL = 'total count'

DETAILS_KEYS = ('failureDetails', 'errorDetails', 'warningDetails')
STATUSES_ORDER = (SUCCESS, FAILURE, ERROR, SKIPPED)
FAILURE_STATUSES = (FAILURE, ERROR)

########################################################################
## Helpers


def _get_path(src: Dict[str, Any], path: List[str]) -> Any:
    if not path:
        return src
    try:
        return _get_path(src[path[0]], path[1:])
    except KeyError:
        return 'KeyError'


def _get_sorted_testcases(
    testcase_metadata: Dict[str, Any], path: List[str]
) -> Dict[str, Any]:
    sorted_testcases = {}
    for testcase, data in testcase_metadata.items():
        sorted_testcases.setdefault(_get_path(data, path), {})[testcase] = data
    return sorted_testcases


def _get_sum_for_status(testcases: Dict[str, Any], status: str) -> int:
    return sum(1 for testcase in testcases.values() if testcase['status'] == status)


def _as_list(what) -> List[str]:
    return [what] if isinstance(what, str) else what


########################################################################
## Datasource: Testcases


def in_scope(expr: str, contexts: Dict[str, Any], scopes_errors: Set[str]) -> bool:
    """Safely evaluate quality gate scope."""
    try:
        return evaluate_bool(expr, contexts)
    except ValueError as err:
        msg = f'Invalid conditional {expr}: {err}.'
        scopes_errors.add(msg)
    except KeyError as err:
        msg = f'Nonexisting context entry in expression {expr}: {err}.'
        scopes_errors.add(msg)
    return False


def get_testresults(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return a possibly empty list of Notifications.

    Each notification in the list is guaranteed to have a
    `spec.testResults` entry.
    """
    return [item for item in events if _has_testresult(item)]


def _has_testresult(item: Dict[str, Any]) -> bool:
    """Determine if a workflow notification has a testResults element."""
    return item.get('kind') == 'Notification' and item.get('spec', {}).get(
        'testResults', False
    )


def _uses_inception(events: List[Dict[str, Any]]) -> bool:
    """Determine if a workflow is the inception workflow."""
    workflow_event = next(
        (event for event in events if event['kind'] == 'Workflow'), None
    )
    if not workflow_event:
        raise ValueError('No Workflow event in workflow events...')
    return any(
        'inception' in _as_list(job['runs-on'])
        for job in workflow_event['jobs'].values()
    )


def _get_inception_testresults(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Get unique testResults notifications for inception workflow.

    Note: This is a kludge until we find a reliable way to map such results
    to the executed tests list.
    """
    unique_results = set()
    unique_events = []
    for event in get_testresults(events):
        event_results = []
        for result in event['spec']['testResults']:
            event_results.append(
                (
                    result['attachment_origin'],
                    result['name'],
                    result['duration'],
                    result['status'],
                )
            )
        if tuple(event_results) not in unique_results:
            unique_results.add(tuple(event_results))
            unique_events.append(event)
    return unique_events


def _get_testresult_params(param_step_id: str, job: Dict[str, Any]) -> Dict[str, Any]:
    """Get .with.data field of param_step_id.

    # Required parameters

    - param_step_id: a string
    - job: a dictionary

    # Returned value

    A dictionary, the `.with.data` part of the params step.

    # Raised exceptions

    An _IndexError_ exception is raised if no params step is found.
    """
    return [
        step['with']['data'] for step in job['steps'] if step.get('id') == param_step_id
    ].pop()


def _create_testresult_labels(
    exec_step: Dict[str, Any],
    job_name: str,
    job: Dict[str, Any],
    parent: Dict[str, Any],
) -> Dict[str, Any]:
    """Create labels for test result.

    # Required parameters

    - exec_step: a dictionary, the 'execute' step
    - job_name: a string (the name of the job containing exec_step)
    - job: a dictionary, the job containing exec_step
    - parent: a dictionary, the event defining the job

    # Returned value

    A labels dictionary.
    """
    exec_step_id = exec_step['id']
    labels = {
        'job': job_name.split()[0],
        'uses': exec_step['uses'],
        'technology': exec_step['uses'].partition('/')[0],
        'runs-on': _as_list(job['runs-on']),
        'managed': False,
    }

    if not (managedtests := parent['metadata'].get('managedTests')):
        return labels
    testcases = managedtests.get('testCases')
    if not testcases or exec_step_id not in testcases:
        if not testcases:
            warning(
                f'Was expecting a "testCases" part in parent of step {exec_step_id}, ignoring.'
            )
        return labels

    labels['managed'] = True
    testcase_metadata = testcases[exec_step_id]
    labels['technology-name'] = testcase_metadata['technology']
    labels['collection'] = managedtests.get('testPlan', {})
    labels.update(
        {
            key: value
            for key, value in testcase_metadata.items()
            if key
            in (
                'name',
                'reference',
                'importance',
                'nature',
                'path',
                'type',
                'uuid',
            )
        }
    )
    try:
        params = _get_testresult_params(testcase_metadata['param_step_id'], job)
        labels['global'] = params.get('global', {})
        labels['data'] = params.get('test', {})
    except IndexError:
        warning(
            f'Could not find "params" step associated to "execute" step {exec_step_id}, ignoring.'
        )
    return labels


def _get_testresult_steporigin(
    attachment_origin: str, events: List[Dict[str, Any]]
) -> Optional[str]:
    """Find the step that produced the attachment.

    # Required parameters

    - attachment_origin: a string (the attachment uuid)
    - events: a list of events

    # Returned value

    A step ID (a string) or None.
    """
    for event in events:
        if not (event['kind'] == 'ExecutionResult' and event.get('attachments')):
            continue
        metadata = event['metadata']
        for value in metadata.get('attachments', {}).values():
            if value['uuid'] != attachment_origin:
                continue
            return (
                metadata['step_origin'][0]
                if metadata['step_origin']
                else metadata['step_id']
            )
    return None


def _get_testresult_labels(
    attachment_origin: str, events: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """Get labels for test result.

    # Required parameters

    - attachment_origin: a string (the attachment uuid)
    - events: a list of events

    # Returned value

    A _labels_ dictionary or None.
    """
    if step_origin := _get_testresult_steporigin(attachment_origin, events):
        jobs_with_steps = {
            job_name + ' ' + event['metadata'].get('job_id', ''): (job, event)
            for event in events
            for job_name, job in event.get('jobs', {}).items()
            if event['kind'] in ('Workflow', 'GeneratorResult') and job.get('steps')
        }
        for job_name, (job, parent) in jobs_with_steps.items():
            for exec_step in job['steps']:
                if exec_step.get('id') == step_origin:
                    return _create_testresult_labels(exec_step, job_name, job, parent)
    return None


def _get_timestamp(
    event: Dict[str, Any], providerid_creationtimestamps: Dict[str, str]
) -> str:
    """Return first provider creationtimestamp or ''.

    # Required parameters

    - event: an ExecutionResult object
    - providerid_creationtimestamps: a dictionary
    """
    for origin_id in event['metadata'].get('step_origin', []):
        if origin_id in providerid_creationtimestamps:
            return providerid_creationtimestamps[origin_id]
    return ''


def _get_testresult_timestamps(
    events: List[Dict[str, Any]],
    testresults: List[Dict[str, Any]],
    testcase_metadata: Dict[str, Any],
):
    """Set timestamp for each testcase in testcase_metadata.

    The timestamp is the one of the originating ProviderResult.
    """
    providerid_creationtimestamps = {
        event['metadata']['step_id']: event['metadata'].get('creationTimestamp', '')
        for event in events
        if event['kind'] == 'ProviderResult'
    }

    origins_results = defaultdict(list)
    for item in testresults:
        for result in item['spec']['testResults']:
            origins_results[result['attachment_origin']].append(result['id'])

    for event in filter(lambda event: event['kind'] == 'ExecutionResult', events):
        for attachment in event['metadata'].get('attachments', {}).values():
            if attachment['uuid'] in origins_results:
                timestamp = _get_timestamp(event, providerid_creationtimestamps)
                for result_id in origins_results[attachment['uuid']]:
                    testcase_metadata[result_id]['timestamp'] = timestamp


def get_testcases(events: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Extract metadata for each test result.

    Test results are Notification events with a `.spec.testResults`
    entry.

    # Required parameters

    - events: a list of events

    # Returned value

    A possibly empty dictionary.  Keys are the testresult IDs, values
    are dictionaries with the following entries:

    - name: a string, the test case name
    - status: a string, the test case status
    - duration: a string, the test case execution time in ms
    - timestamp: a string, provider creation timestamp
    - test: a dictionary, the test case metadata
    - failureDetails|errorDetails|warningDetails: a dictionary with test
      case failure details
    - errorsList: a Robot Framework specific list with execution general
      errors

    `testcases` is a dictionary of entries like:

    ```
    "<<<testcase_uuid>>>": {
        "name": "<<<[Test suite#]Test case name>>>",
        "status": "<<<SUCCESS|FAILURE|ERROR|SKIPPED>>>",
        "duration": "<<<test execution time in ms>>>",
        "timestamp": "<<<provider creation timestamp>>>"
        "test": {
            "job": "<<<job name>>>",
            "uses": "<<<provider function>>>",
            "technology": "<<<test technology>>>",
            "runs-on": [<<<list of execution environment tags>>>],
            "managed": boolean, True for test cases managed by a test referential
            "status": "<<<SUCCESS|FAILURE|ERROR|SKIPPED>>>"
        },
        "failureDetails"|"errorDetails"|"warningDetails": {
            "message": "<<<error message>>>",
            "type": "<<<error type>>>",
            "text": "<<<error trace>>>"
        },
        "errorsList": [
            {
                "message": "<<<Robot Framework general error message>>>",
                "timestamp": "<<<Robot Framework error message timestamp>>>"
            }
        ]
    }
    ```

    # Raised exceptions

    A _ValueError_ exception is raised if there were no test results in
    `events`.
    """
    testcases = {}
    results = False
    if _uses_inception(events):
        testresults = _get_inception_testresults(events)
    else:
        testresults = get_testresults(events)

    for testresult in testresults:
        results = True
        labels = _get_testresult_labels(
            testresult['metadata']['attachment_origin'][0], events
        )
        if not labels:
            continue
        for testcase in testresult['spec']['testResults']:
            testcases[testcase['id']] = {
                'name': testcase['name'],
                'status': testcase['status'],
                'duration': testcase.get('duration', 0),
                'test': labels.copy(),
            }
            testcases[testcase['id']]['test']['status'] = testcase['status']
            data = {}
            if testcase['status'] in FAILURE_STATUSES:
                data = {key: testcase[key] for key in DETAILS_KEYS if testcase.get(key)}
            if testcase.get('errorsList'):
                data['errorsList'] = testcase['errorsList']
            testcases[testcase['id']].update(data)
    if not results:
        raise ValueError('No test results in events.')
    _get_testresult_timestamps(events, testresults, testcases)
    return testcases


########################################################################
## Datasource: Tags


def get_tags(
    events: List[Dict[str, Any]], testcase_metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Extract metadata for each execution environment tag.

    # Required parameters:

    - events: a list of events

    # Returned value:

    A dictionary. Keys are tags names, values are dictionaries with testcase
    by tag status counters.

    `tags` is a dictionary of entries like:

    ```
    "<<<tag name>>>": {
        "FAILURE": <<<failed tests count>>>,
        "SUCCESS": <<<passed tests count>>>,
        "SKIPPED": <<<skipped tests count>>>,
        "ERROR": <<<technical KO tests count>>>,
        'total': <<<total tests count>>>,
        'other': <<<SKIPPED + ERROR tests count>>>
    }
    ```
    """
    try:
        testcase_metadata = testcase_metadata or get_testcases(events)
    except ValueError as err:
        raise ValueError(str(err) + ' Cannot extract metadata for tags.')
    tags = {}
    for testcase in testcase_metadata.values():
        for tag in testcase['test']['runs-on']:
            tags.setdefault(tag, {SUCCESS: 0, FAILURE: 0, ERROR: 0, SKIPPED: 0})
            tags[tag][testcase['status']] += 1
    for tag, counts in tags.items():
        counts['total'] = sum(counts[status] for status in STATUSES_ORDER)
        counts['other'] = sum(counts[status] for status in (SKIPPED, ERROR))
        tags[tag] = {k.lower(): v for k, v in counts.items()}
    return tags


########################################################################
## Datasource: Jobs


def _evaluate_test_results(jobs_testcases: Dict[str, Any]) -> Dict[str, Any]:
    """Summarize job testcases.

    # Returned value

    A dictionary with one entry per job (a dictionary with keys being
    statuses and values being counts).
    """
    summaries = {}
    for job, testcases in jobs_testcases.items():
        successes, failures, errors, skipped = [
            _get_sum_for_status(testcases, status) for status in STATUSES_ORDER
        ]
        summaries[job] = {
            SUCCESS: successes,
            FAILURE: failures,
            ERROR: errors,
            SKIPPED: skipped,
            TOTAL: len(testcases),
        }
    return summaries


def get_jobs(
    events: List[Dict[str, Any]], testcase_metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Extract metadata for each job.

    # Required parameters:

    - events: a list of events

    # Returned value:

    A dictionary. Keys are job names, values are dictionaries with the
    following entries:

    - name: a string, job name
    - runs-on: a list, execution environment tags
    - testcases: a dictionary, job-related test cases
    - counts: a dictionary, tests statuses count by job
    - variables: a dictionary, job-related environment variables

    `jobs_testcases` is a dictionary of entries like:

    ```
    "<<<job_name>>>": {
        "runs-on": [<<<execution environment tags>>>],
        "counts": {
            "FAILURE": <<<failed tests count>>>,
            "SUCCESS": <<<passed tests count>>>,
            "ERROR": <<<technical KOs count>>>,
            "SKIPPED": <<<skipped tests count>>>,
            "total count": <<<total tests count>>>
        },
        "variables": {
            "<<<variable name>>>": "<<<variable value>>>",
            ...
        }
    }
    ```
    """
    try:
        testcase_metadata = testcase_metadata or get_testcases(events)
    except ValueError as err:
        raise ValueError(str(err) + ' Cannot extract metadata for jobs.')
    jobs_testcases = _get_sorted_testcases(testcase_metadata, ['test', 'job'])
    if 'KeyError' in jobs_testcases:
        raise ValueError('Cannot get jobs-ordered dataset from testcases.')
    job_events = [
        event
        for event in events
        if event['kind'] == 'ExecutionCommand'
        and event['metadata']['step_sequence_id'] == -1
        and event['metadata']['name'] in jobs_testcases
    ]
    results = _evaluate_test_results(jobs_testcases)
    jobs = {}
    for job in job_events:
        job_name = job['metadata']['name']
        jobs.setdefault(
            job['metadata']['name'],
            {
                'runs-on': job['runs-on'],
                'counts': results[job_name],
                'variables': {
                    name: value for name, value in job.get('variables', {}).items()
                },
            },
        )
    return jobs
