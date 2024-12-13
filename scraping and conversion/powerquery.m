let
    // Define the start and end dates
    StartDate = #date(2024, 11, 20),
    EndDate = #date(2024, 12, 10),

    // Generate a list of dates between StartDate and EndDate
    DateList = List.Dates(StartDate, Duration.Days(EndDate - StartDate) + 1, #duration(1, 0, 0, 0)),

    // Convert dates to text in the required format (e.g., DD/MM/YYYY)
    DateStrings = List.Transform(DateList, each Text.PadStart(Text.From(Date.Day()), 2, "0") & "/" & Text.PadStart(Text.From(Date.Month()), 2, "0") & "/" & Text.From(Date.Year(_))),

    // Construct the URLs by appending the date strings to the base URL
    BaseUrl = "https://www.delhisldc.org/Loaddata.aspx?mode=",
    UrlList = List.Transform(DateStrings, each BaseUrl & _),

    // Load data from each URL
    LoadDataFromUrls = List.Transform(UrlList, each 
        let
            Source = try Web.BrowserContents(_) otherwise null
        in
            Source
    ),

    // Convert the content to tables and add the corresponding date as a column
    ExtractedTables = List.Transform(LoadDataFromUrls, (content, idx) =>
        if content <> null then
            let
                TableData = Csv.Document(content, [Delimiter=",", Encoding=65001]),
                TableWithDate = Table.AddColumn(TableData, "Date", each DateStrings{idx})
            in
                TableWithDate
        else
            null
    )
in
    ExtractedTables
