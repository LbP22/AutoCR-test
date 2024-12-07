PROMPT="""
Make the code review of provided dump of github repository.
Notice, that the code author level is {CANDIDATE_LEVEL} and the assignment description is "{ASSIGNEMENT_DESCRIPTION}".
The review must include this parts: 1. Analyzed files list. 2. Downsides/advantages/annotations. 3. Rating from 1 to 5. 4. Conclusion.
Here is the dump of the repository:
{REPO_DUMP}
"""