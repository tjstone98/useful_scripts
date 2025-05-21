def group_by_quarter(df, agg_type):
    """
    Purpose: Aggregate columns by fiscal quarter.
    Inputs: Dataframe with monthly columns to aggregate. Monthly columns must begin YYYYMM.
    Outputs: Additional columns in the dataframe representing the quarterly aggregation.
    """
    # Extract years represented in dataframe.
    years = sorted(list(set([col[0:4] for col in df.columns if col.startswith(('19', '20'))])))
    print(f'Years represented: {years}')

    month_to_quarter_dict = {
        '01': 'Q1',
        '02': 'Q1',
        '03': 'Q1',
        '04': 'Q2',
        '05': 'Q2',
        '06': 'Q2',
        '07': 'Q3',
        '08': 'Q3',
        '09': 'Q3',
        '10': 'Q4',
        '11': 'Q4',
        '12': 'Q4'
    }

    for year in years:
        year_cols = [col for col in df.columns if col.startswith(year)]
        
        # Group columns by quarter.
        for quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
            quarter_cols = [col for col in year_cols if col[4:6] in month_to_quarter_dict and month_to_quarter_dict[col[4:6]] == quarter]

            if quarter_cols:
                quarter_col_name = f'{year}{quarter}'

                if agg_type == 'sum':
                    df[quarter_col_name] = df[quarter_cols].sum(axis=1)
                elif agg_type == 'mean':
                    df[quarter_col_name] = df[quarter_cols].mean(axis=1)
                else:
                    raise ValueError(f'Unsupported aggregation type: {agg_type}.')
    return df
