SELECT t1.ticker, t1.trade_date, t1.volume, avg(t2.volume) from trade_histories as t1 join trade_histories as t2 on t1.ticker = t2.ticker and t2.trade_date between DATE_SUB(t1.trade_date,INTERVAL 5 DAY) and t1.trade_date GROUP BY t1.ticker, t1.trade_date, t1.volume;

SELECT t1.ticker, t1.trade_date, t1.high, avg(t2.high) from trade_histories as t1 join trade_histories as t2 on t1.ticker = t2.ticker and t2.trade_date between DATE_SUB(t1.trade_date,INTERVAL 5 DAY) and t1.trade_date GROUP BY t1.ticker, t1.trade_date, t1.high;

SELECT t1.ticker, t1.trade_date, t1.low, avg(t2.low) from trade_histories as t1 join trade_histories as t2 on t1.ticker = t2.ticker and t2.trade_date between DATE_SUB(t1.trade_date,INTERVAL 5 DAY) and t1.trade_date GROUP BY t1.ticker, t1.trade_date, t1.low;

SELECT t1.ticker, t1.trade_date, t1.open, avg(t2.open) from trade_histories as t1 join trade_histories as t2 on t1.ticker = t2.ticker and t2.trade_date between DATE_SUB(t1.trade_date,INTERVAL 5 DAY) and t1.trade_date GROUP BY t1.ticker, t1.trade_date, t1.open;

SELECT t1.ticker, t1.trade_date, t1.volume, avg(t2.volume) from trade_histories as t1 join trade_histories as t2 on t1.ticker = t2.ticker and t2.trade_date between DATE_SUB(t1.trade_date,INTERVAL 50 DAY) and t1.trade_date GROUP BY t1.ticker, t1.trade_date, t1.volume;

SELECT t1.ticker, t1.trade_date, t1.high, avg(t2.high) from trade_histories as t1 join trade_histories as t2 on t1.ticker = t2.ticker and t2.trade_date between DATE_SUB(t1.trade_date,INTERVAL 50 DAY) and t1.trade_date GROUP BY t1.ticker, t1.trade_date, t1.high;

SELECT t1.ticker, t1.trade_date, t1.low, avg(t2.low) from trade_histories as t1 join trade_histories as t2 on t1.ticker = t2.ticker and t2.trade_date between DATE_SUB(t1.trade_date,INTERVAL 50 DAY) and t1.trade_date GROUP BY t1.ticker, t1.trade_date, t1.low;

SELECT t1.ticker, t1.trade_date, t1.open, avg(t2.open) from trade_histories as t1 join trade_histories as t2 on t1.ticker = t2.ticker and t2.trade_date between DATE_SUB(t1.trade_date,INTERVAL 50 DAY) and t1.trade_date GROUP BY t1.ticker, t1.trade_date, t1.open;