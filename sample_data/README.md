# Assignment #2 - Sample Files

This gist contains the sample data, query, and validation function for
Assignment #2 (LangGraph code generation with reflection and validation).

## Files in this gist

| File                       | Purpose                                                |
|----------------------------|--------------------------------------------------------|
| `customers.csv`            | Sample customer records                                |
| `products.csv`             | Sample product catalog                                 |
| `orders.csv`               | Sample order history                                   |
| `query_input.txt`          | Describes the query name and the data files           |
| `top-spender.txt`          | The query your LangGraph must answer                   |
| `top_spender_validate.py`  | Validation function — your LangGraph must call this    |
| `prepare_dataset.py`       | Run once to verify all files are present               |
| `README.md`                | This file                                              |

## Setup

1. Download all 8 files from this gist into a single directory.
2. From that directory, run:
   ```
   python prepare_dataset.py
   ```
   You should see: `All 6 required files found. You are ready to start working on hw2.py.`

3. Place your `hw2.py` (your LangGraph application) in the same directory.
4. Run your application with:
   ```
   python hw2.py
   ```

## What your `hw2.py` must do

Your application must:

1. Read `query_input.txt` to discover the query name (`top-spender`) and the data files.
2. Read `top-spender.txt` to get the actual query.
3. Use the LLM to generate a Python program that answers the query against the CSV files.
4. Execute that program. If it crashes or produces invalid JSON, reflect and regenerate (up to 4 retries).
5. After successful execution, **import `top_spender_validate.py` and call `top_spender_answer(answer)`**.
   - If it returns `True`, you are done.
   - If it returns `False`, treat it as an error and enter the reflection loop.
6. Write the 4 output files: `top-spender.py`, `top-spender_answer.txt`,
   `top-spender_errors.txt`, `top-spender_reflect.txt`.

## Expected correct answer

For the sample `top-spender` query, the correct JSON answer is:

```json
{
  "FirstName": "Oren",
  "LastName": "Levi",
  "City": "Haifa",
  "TotalSpent": 572.47
}
```

## Important notes

- The grader will test your code with **different queries** and **different data files**
  (with the same general format). Do not hardcode anything specific to `top-spender`
  or to these CSV files.
- The query name in the input file determines the names of all output files and
  the validation function. Hyphens in the query name (`top-spender`) become
  underscores in the validation file name (`top_spender_validate.py`) and the
  function name (`top_spender_answer`).
- Do NOT submit the files from this gist with your assignment. The grader will
  provide their own sample files when grading.
