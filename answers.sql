/******************************************************************************/
/* Fabian Pascal                                                              */
/* Indicate your student number here: A0187652U                               */
/******************************************************************************/
SELECT per.empid, per.lname 
FROM employee per, payroll pay
WHERE per.empid = pay.empid 
AND pay.salary = 189170
ORDER BY per.empid, per.lname;
-- Average Planning 0.14 ms
-- Average Execution 5.51 ms

/******************************************************************************/
/* Answer Question 2.a below                                                  */
/******************************************************************************/
SELECT per.empid, per.lname
FROM employee per FULL OUTER JOIN payroll pay 
    ON per.empid = pay.empid AND pay.salary = 189170
WHERE per.empid IS NOT NULL AND pay.empid IS NOT NULL
ORDER BY per.empid, per.lname;
-- Average Planning 0.15 ms
-- Average Execution 5.89 ms

/******************************************************************************/
/* Answer Question 2.b below                                                  */
/******************************************************************************/
SELECT per.empid, per.lname
FROM employee per, (SELECT * FROM payroll WHERE salary = 189170) AS temp
WHERE per.empid = temp.empid
ORDER BY per.empid, per.lname;
-- Average Planning 0.16 ms
-- Average Execution 5.75 ms

/******************************************************************************/
/* Answer Question 2.c below                                                  */
/******************************************************************************/
SELECT per.empid, per.lname
FROM employee per
WHERE per.empid NOT IN (
    SELECT empid
	FROM employee
	WHERE empid NOT IN (
		SELECT empid
		FROM payroll
	)
	UNION
	SELECT per.empid
	FROM employee per, payroll pay
	WHERE per.empid = pay.empid AND pay.salary != 189170
)
ORDER BY per.empid, per.lname;
-- Average Planning 0.24 ms
-- Average Execution 45.07 ms

/******************************************************************************/
/* Answer Question 3 below                                                  */
/******************************************************************************/
SELECT per.empid, per.lname
FROM employee per
WHERE (
	SELECT COUNT(*) FROM payroll pay WHERE pay.empid = per.empid AND pay.salary = 189170
) > 0
ORDER BY per.empid, per.lname

-- Indicate the average measured time for 20 executions for the query.
-- (replace <time> with the average time reported by test function).
-- Average Planning 0.11 ms
-- Average Execution 21678.86 ms

EXPLAIN ANALYZE SELECT per.empid, per.lname 
FROM employee per, payroll pay
WHERE per.empid = pay.empid 
AND pay.salary = 189170
ORDER BY per.empid, per.lname;

EXPLAIN ANALYZE SELECT per.empid, per.lname 
FROM employee per FULL OUTER JOIN payroll pay 
ON per.empid = pay.empid AND pay.salary = 189170
WHERE per.empid IS NOT NULL AND pay.empid IS NOT NULL
ORDER BY per.empid, per.lname

EXPLAIN ANALYZE SELECT per.empid, per.lname 
FROM employee per, (SELECT * FROM payroll WHERE salary = 189170) pay
WHERE per.empid = pay.empid
ORDER BY per.empid, per.lname;

EXPLAIN ANALYZE SELECT per.empid, per.lname 
FROM employee per
WHERE per.empid IN (
	SELECT pay.empid
	FROM payroll pay
	WHERE pay.salary = 189170
)
ORDER BY per.empid, per.lname;

EXPLAIN ANALYZE SELECT per.empid, per.lname 
FROM employee per
WHERE EXISTS (
	SELECT *
	FROM payroll pay
	WHERE pay.empid = per.empid
	AND pay.salary = 189170
)
ORDER BY per.empid, per.lname;

EXPLAIN ANALYZE SELECT per.empid, per.lname 
FROM employee per
WHERE NOT EXISTS (
	SELECT 1
	FROM payroll pay
	WHERE pay.empid = per.empid
	AND pay.salary != 189170
)
ORDER BY per.empid, per.lname;

-- Third slowest, sequential scan on payroll
EXPLAIN ANALYZE SELECT per.empid, per.lname 
FROM employee per
WHERE per.empid NOT IN (
	SELECT pay.empid
	FROM payroll pay
	WHERE pay.salary != 189170
)
ORDER BY per.empid, per.lname;

-- Second Slowest so far, sequential scan on payroll: 0.057, 6754
EXPLAIN ANALYZE SELECT per.empid, per.lname 
FROM employee per
WHERE (
	SELECT pay.salary
	FROM payroll pay
	WHERE pay.empid = per.empid
) = 189170
ORDER BY per.empid, per.lname;

-- Slowest so far, sequential scan on payroll, then aggregate: 0.129, 7675
EXPLAIN ANALYZE SELECT per.empid, per.lname 
FROM employee per
WHERE (
	SELECT COUNT(*)
	FROM payroll pay
	WHERE pay.empid = per.empid AND pay.salary = 189170
) > 0
ORDER BY per.empid, per.lname;

-- Slowest so far, Sequential scan on payroll: 0.062, 7425 
EXPLAIN ANALYZE SELECT per.empid, per.lname
FROM employee per
WHERE (
	SELECT pay.empid
	FROM payroll pay
	WHERE pay.empid = per.empid AND pay.salary = 189170
) IS NOT NULL
ORDER BY per.empid, per.lname;