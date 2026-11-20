\echo '------------------------------------------------------------'

\echo 'Refreshing Materialized views:\n'

\echo 'Refreshing offer purchase view'
REFRESH MATERIALIZED VIEW analytics.mv_offer_purchases;
\echo '------------------------------------------------------------'


\echo 'Refreshing offer consumption view'
REFRESH MATERIALIZED VIEW analytics.mv_offer_consumption;
\echo '------------------------------------------------------------'

