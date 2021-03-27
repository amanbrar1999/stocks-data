warnings;

drop table if exists StockIpoData;
drop table if exists StockHistory;
drop table if exists Stocks;

select '----------------------------------------------------------------' as '';
select 'Create Stocks' as '';

create table Stocks (
    ticker char(10),
    primary key (ticker)
);

load data infile '/var/lib/mysql-files/data/AMEX_NYSE_NASDAQ_stonks/all_symbols.csv' ignore into table Stocks
    lines terminated by '\n'
    (ticker);

select '----------------------------------------------------------------' as '';
select 'Create Stock IPO' as '';

create table StockIpoData (
    ticker char(10),
    ipoDate date,
    highDay0 double,
    openDay0 double,
    lowDay0 double,
    volumeDay0 double,
    primary key (ticker)
);

load data infile '/var/lib/mysql-files/data/IPODataProcessed.csv' ignore into table StockIpoData
    fields terminated by ','
    lines terminated by '\n'
    ignore 1 lines
    (ticker,@year,@month,@day,highDay0,openDay0,lowDay0,volumeDay0)
    set ipoDate = CAST(CONCAT(@year,"-",@month, "-", @day) as date);

-- select '----------------------------------------------------------------' as '';
-- select 'Create Stock History' as '';

-- create table StockHistory (
--     ticker char(10),
--     date datetime,
--     volume bigint, -- changed from INT to BIGINT because 1 value exceeded int max
--     open double,
--     high double,
--     low double,
--     close double,
--     adjclose double,
--     primary key (ticker, date),
--     foreign key (ticker) references Stocks(ticker)
-- );

-- load data infile '/var/lib/mysql-files/data/AMEX_NYSE_NASDAQ_stonks/fh_5yrs.csv' ignore into table StockHistory
--     fields terminated by ','
--     lines terminated by '\n'
--     ignore 1 lines
--     (date,volume,open,high,low,close,adjclose,ticker);