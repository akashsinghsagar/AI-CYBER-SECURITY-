# Data

The project uses the NSL-KDD-style files `Train_data.csv` and `Test_data.csv`.

* `Train_data.csv` contains 41 network connection features plus the `class` target
  (`normal` or `anomaly`).
* `Test_data.csv` contains the same 41 features without labels and is used for
  optional prediction export.

The original CSVs are kept at the project root for compatibility with the
provided notebook. Copy them into this folder before running the pipeline if
you want a self-contained `data/` directory:

```powershell
Copy-Item ..\Train_data.csv .\Train_data.csv
Copy-Item ..\Test_data.csv .\Test_data.csv
```

These files are derived from the NSL-KDD network intrusion dataset. Use them
only for educational analysis and do not treat model output as an automated
security decision.

