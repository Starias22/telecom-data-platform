-- Offer revenue
SELECT
    offer_type,
    price_xof,
    SUM(revenue) AS total_revenue
FROM dw.fact_purchase AS fp
JOIN dw.dim_offer AS dof
    ON dof.offer_config_id = fp.offer_config_id
JOIN dw.dim_date AS dd
    ON dd.date_key = fp.date_key
WHERE full_date BETWEEN '2020-01-01' -- Period start
                        AND '2020-05-31' -- Period end
GROUP BY
    offer_type,
    price_xof
ORDER BY
    offer_type,
    price_xof
;