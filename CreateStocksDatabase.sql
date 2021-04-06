warnings;

drop table if exists history_comments;
drop table if exists article_comments;
drop table if exists finance_comments;
drop table if exists general_comments;
drop table if exists comment_tags;
drop table if exists comment_tickers;
drop table if exists comments;
drop table if exists users;
drop table if exists article_tickers;
drop table if exists articles;
drop table if exists company_annual_finances;
drop table if exists trade_histories;
drop table if exists stocks;

-- First create the tables that have data that will be filled in by the stocks csvs

select '----------------------------------------------------------------' as '';
select 'Create stocks' as '';

create table stocks (
    ticker varchar(10),
    ipoDate date,
    highDay0 double,
    openDay0 double,
    lowDay0 double,
    volumeDay0 double,
    primary key (ticker)
);

load data infile '/var/lib/mysql-files/data/IPODataProcessed.csv' ignore into table stocks
    fields terminated by ','
    lines terminated by '\n'
    ignore 1 lines
    (ticker,@year,@month,@day,highDay0,openDay0,lowDay0,volumeDay0)
    set ipoDate = CAST(CONCAT(@year,"-",@month, "-", @day) as date);

load data infile '/var/lib/mysql-files/data/AMEX_NYSE_NASDAQ_stonks/all_symbols.csv' ignore into table stocks
    lines terminated by '\n'
    (ticker);

select '----------------------------------------------------------------' as '';
select 'Create company_annual_finances' as '';

create table company_annual_finances (
    ticker varchar(10), -- NOTE that the column "ticker" in the finance csvs contained values but was unnamed, this was changed to be named ticker from process_financial_data.py
    fiscal_year int,
    revenue double,
    revenue_growth double,
    cost_of_revenue double,
    gross_profit double,
    sga_expense double,
    operating_expense double,
    operating_income double,
    interest_expense double,
    primary key (ticker, fiscal_year),
    foreign key (ticker) references stocks(ticker)
);

create index idx_fiscal_year on company_annual_finances(fiscal_year);

load data infile '/var/lib/mysql-files/data/financial_data_processed/All_Financial_Data.csv' ignore into table company_annual_finances
    fields terminated by ','
    lines terminated by '\n'
    ignore 1 lines
    (ticker,fiscal_year,revenue,revenue_growth,cost_of_revenue,gross_profit,sga_expense,operating_expense,operating_income,interest_expense);

select '----------------------------------------------------------------' as '';
select 'Create trade_histories' as '';

create table trade_histories (
    ticker varchar(10),
    trade_date datetime,
    volume bigint, -- changed from INT to BIGINT because 1 value exceeded int max
    open double,
    high double,
    low double,
    close double,
    adjclose double,
    primary key (ticker, trade_date),
    foreign key (ticker) references stocks(ticker)
);

create index idx_trade_date on trade_histories(trade_date);

load data infile '/var/lib/mysql-files/data/AMEX_NYSE_NASDAQ_stonks/fh_5yrs.csv' ignore into table trade_histories
    fields terminated by ','
    lines terminated by '\n'
    ignore 1 lines
    (trade_date,volume,open,high,low,close,adjclose,ticker);

select '----------------------------------------------------------------' as '';
select 'Create articles' as '';

create table articles (
    url varchar(500),
    headline varchar(500),
    date datetime,
    publisher varchar(255),
    primary key (url)
);

load data infile '/var/lib/mysql-files/data/articles/raw_partner_headlines.csv' ignore into table articles
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines
    (@throwaway,headline,url,publisher,date,@throwaway);

load data infile '/var/lib/mysql-files/data/articles/raw_analyst_ratings.csv' ignore into table articles
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines
    (@throwaway,headline,url,publisher,date,@throwaway);

select '----------------------------------------------------------------' as '';
select 'Create article_tickers' as '';

create table article_tickers (
    url varchar(500),
    ticker varchar(10),
    primary key (url, ticker),
    foreign key (url) references articles(url),
    foreign key (ticker) references stocks(ticker)
);

load data infile '/var/lib/mysql-files/data/articles/raw_partner_headlines.csv' ignore into table article_tickers
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines
    (@throwaway,@throwaway,url,@throwaway,@throwaway,ticker);

load data infile '/var/lib/mysql-files/data/articles/raw_analyst_ratings.csv' ignore into table article_tickers
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines
    (@throwaway,@throwaway,url,@throwaway,@throwaway,ticker);

-- Next create the tables for which there is no initial data

select '----------------------------------------------------------------' as '';
select 'Create users' as '';

create table users (
    user_id int not null AUTO_INCREMENT,
    name varchar(255),
    priv boolean,
    primary key (user_id)
);

select '----------------------------------------------------------------' as '';
select 'Create comments' as '';

create table comments (
    comment_id int not null AUTO_INCREMENT,
    user_id int not null,
    created_at datetime,
    last_updated_at datetime,
    message varchar(255),
    primary key (comment_id),
    foreign key (user_id) references users(user_id)
);

select '----------------------------------------------------------------' as '';
select 'Create comment_tickers' as '';

create table comment_tickers (
    comment_id int not null,
    ticker varchar(10),
    primary key (comment_id, ticker),
    foreign key (comment_id) references comments(comment_id),
    foreign key (ticker) references stocks(ticker)
);

select '----------------------------------------------------------------' as '';
select 'Create comment_tags' as '';

create table comment_tags (
    comment_id int not null,
    tag varchar(255),
    primary key (comment_id, tag),
    foreign key (comment_id) references comments(comment_id)
);

select '----------------------------------------------------------------' as '';
select 'Create general_comments' as '';

create table general_comments (
    comment_id int not null,
    primary key (comment_id),
    foreign key (comment_id) references comments(comment_id)
);

select '----------------------------------------------------------------' as '';
select 'Create finance_comments' as '';

create table finance_comments (
    comment_id int not null,
    fiscal_year int,
    primary key (comment_id),
    foreign key (comment_id) references comments(comment_id),
    foreign key (fiscal_year) references company_annual_finances(fiscal_year)
);

select '----------------------------------------------------------------' as '';
select 'Create article_comments' as '';

create table article_comments (
    comment_id int not null,
    url varchar(255),
    primary key (comment_id),
    foreign key (comment_id) references comments(comment_id),
    foreign key (url) references articles(url)
);

select '----------------------------------------------------------------' as '';
select 'Create history_comments' as '';

create table history_comments (
    comment_id int not null,
    trade_date datetime,
    primary key (comment_id),
    foreign key (comment_id) references comments(comment_id),
    foreign key (trade_date) references trade_histories(trade_date)
);

