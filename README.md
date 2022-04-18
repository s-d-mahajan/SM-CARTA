# `SM-CARTA`

A CLI tool to read capitalization table and output vesting schedule for give csv data.

# Installation
- Unzip the `SM-CARTA.zip` file 
- Run `$cd SM-CARTA`
- Run `$pip install --editable .`

# Usage 
- Use `$captable <file_path> <target_date> <decimal_precision>` to get the vesting schedule
- Run `$captable example.csv 2027-02-01  4` (*You need to be in SM-CARTA directory*)
- Contents of example.csv
```
VEST,E001,Alice Smith,ISO-001,2020-01-01,1000
VEST,E001,Alice Smith,ISO-001,2021-01-01,1000
VEST,E001,Alice Smith,ISO-002,2020-03-01,300
VEST,E001,Alice Smith,ISO-002,2020-04-01,500
CANCEL,E001,Alice Smith,ISO-001,2021-01-01,700
VEST,E002,Bobby Jones,NSO-001,2020-01-02,100
VEST,E002,Bobby Jones,NSO-001,2020-02-02,200
VEST,E002,Bobby Jones,NSO-001,2020-03-02,300.677
VEST,E003,Cat Helms,NSO-002,2024-01-01,100.344
```
- STDOUT 
``` 
E001,Alice Smith,ISO-001,1300
E001,Alice Smith,ISO-002,800
E002,Bobby Jones,NSO-001,601
E003,Cat Helms,NSO-002,100
````

# Testing 
- Run `$cd SM-CARTA`
- Run `$pytst .`

# Future Usages 
- This can easily be modified to get schedule of just one employee 
- To get schedule between date range
