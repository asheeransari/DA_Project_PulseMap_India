-- PulseMap India — Business Queries
-- Author: Asheer Ahmad
-- Database: SQLite (pulsemap.db)

-- ============================================
-- Query 1: Top 10 Critical Risk Districts
-- ============================================
SELECT 
    d.district,
    d.state,
    r.risk_score,
    r.risk_tier
FROM districts d
JOIN risk_scores r ON d.id = r.district_id
WHERE r.risk_tier = 'Critical Risk'
ORDER BY r.risk_score DESC
LIMIT 10;

-- ============================================
-- Query 2: State-wise Risk Tier Distribution
-- ============================================
SELECT
    d.state,
    COUNT(CASE WHEN r.risk_tier = 'Critical Risk' THEN 1 END) AS critical,
    COUNT(CASE WHEN r.risk_tier = 'High Risk' THEN 1 END) AS high,
    COUNT(CASE WHEN r.risk_tier = 'Moderate Risk' THEN 1 END) AS moderate,
    COUNT(CASE WHEN r.risk_tier = 'Low Risk' THEN 1 END) AS low,
    COUNT(*) AS total_districts,
    ROUND(AVG(r.risk_score), 2) AS avg_risk_score
FROM districts d
JOIN risk_scores r ON d.id = r.district_id
GROUP BY d.state
ORDER BY avg_risk_score DESC;

-- ============================================
-- Query 3: State-wise Risk Ranking (Window Function)
-- ============================================
SELECT
    d.state,
    d.district,
    r.risk_score,
    r.risk_tier,
    RANK() OVER (
        PARTITION BY d.state 
        ORDER BY r.risk_score DESC
    ) AS state_rank
FROM districts d
JOIN risk_scores r ON d.id = r.district_id
ORDER BY d.state, state_rank;

-- ============================================
-- Query 4: Top 3 Highest Risk Districts Per State (CTE)
-- ============================================
WITH ranked_districts AS (
    SELECT
        d.district,
        d.state,
        r.risk_score,
        r.risk_tier,
        ROW_NUMBER() OVER (
            PARTITION BY d.state
            ORDER BY r.risk_score DESC
        ) AS rn
    FROM districts d
    JOIN risk_scores r ON d.id = r.district_id
)
SELECT district, state, risk_score, risk_tier
FROM ranked_districts
WHERE rn <= 3
ORDER BY state, risk_score DESC;

-- ============================================
-- Query 5: Anaemia vs Literacy Comparison
-- ============================================
SELECT
    d.district,
    d.state,
    h.anaemia_w,
    s.literacy_w,
    r.risk_tier,
    CASE 
        WHEN s.literacy_w >= 80 THEN 'High Literacy'
        WHEN s.literacy_w >= 60 THEN 'Medium Literacy'
        ELSE 'Low Literacy'
    END AS literacy_group
FROM districts d
JOIN health_metrics h ON d.id = h.district_id
JOIN socioeconomic s ON d.id = s.district_id
JOIN risk_scores r ON d.id = r.district_id
ORDER BY h.anaemia_w DESC;

-- ============================================
-- Query 6: Cancer Screening Gap Analysis (CTE)
-- ============================================
WITH screening_avg AS (
    SELECT
        d.state,
        ROUND(AVG(h.cervical_screening_w), 2) AS avg_cervical,
        ROUND(AVG(h.breast_exam_w), 2) AS avg_breast,
        ROUND(AVG(h.oral_exam_w), 2) AS avg_oral,
        ROUND(AVG(h.cervical_screening_w + 
                  h.breast_exam_w + 
                  h.oral_exam_w) / 3, 2) AS overall_screening
    FROM districts d
    JOIN health_metrics h ON d.id = h.district_id
    GROUP BY d.state
)
SELECT *,
    RANK() OVER (ORDER BY overall_screening ASC) AS screening_rank
FROM screening_avg
ORDER BY overall_screening ASC;

-- ============================================
-- Query 7: Gender Health Gap
-- ============================================
SELECT
    d.state,
    ROUND(AVG(h.blood_sugar_w), 2) AS avg_bs_women,
    ROUND(AVG(h.blood_sugar_m), 2) AS avg_bs_men,
    ROUND(AVG(h.blood_sugar_m) - AVG(h.blood_sugar_w), 2) AS bs_gap,
    ROUND(AVG(h.bp_elevated_w), 2) AS avg_bp_women,
    ROUND(AVG(h.bp_elevated_m), 2) AS avg_bp_men,
    ROUND(AVG(h.bp_elevated_m) - AVG(h.bp_elevated_w), 2) AS bp_gap
FROM districts d
JOIN health_metrics h ON d.id = h.district_id
GROUP BY d.state
ORDER BY bp_gap DESC;