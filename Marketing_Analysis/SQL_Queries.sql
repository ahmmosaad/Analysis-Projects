

-- Prodcuts Table 

-- original Data 
select * from products

-- categorise products upon price

select 
ProductID,
ProductName,
Category,
Price,

CASE
WHEN Price < 50 then 'Low'
when price between 50 and 200 then 'Medium'
else 'High' 
end As PriceCategory

from products



-- ***************************************************************

-- Customers Table

select * from customers
select * from geography
-- asign city and country to customer using geography table
select * from geography


select 
c.CustomerID, c.CustomerName, c.Gender, c.Age, g.Country, g.City

from customers as c left join geography as g

on c.GeographyID = g.GeographyID


-- ***************************************************************************************************
-- Customer Reviews Table
select * from customer_reviews

-- jsut i will replace double speces in Review text with one space

select ReviewID, CustomerID, ProductID, ReviewDate, REPLACE(ReviewText, '  ', ' ') as ReviewText
from customer_reviews




-- ********************************************************************************************
-- Customer Journey Table

select * from customer_journey
-- i wants to check duplication here so 

-- make CTE common table Expresion
with DupilcatedRecordes as (
select 
JourneyID, CustomerID, ProductID, VisitDate, Stage, Action, Duration,
AVG(Duration) OVER (PARTITION BY VisitDate) AS avg_duration,
ROW_NUMBER() over ( PARTITION BY   JourneyID, CustomerID, ProductID, VisitDate, Stage, Action order by JourneyID ) as row_num
from customer_journey
)

select 

    JourneyID,  
	CustomerID,  
    ProductID,  
    VisitDate,  
    UPPER(Stage) as Stage,  
    Action,  
	COALESCE(Duration, avg_duration) AS Duration 

from DupilcatedRecordes
where row_num = 1



-- ****************************************************************************

-- Engagement Data Table

select * from engagement_data

-- separate view and clicks
-- uppercase all content type
-- excluse newsletter content type cause its out of analysis scope

select 

EngagementID,
ContentID, 
UPPER(ContentType) as ContentType,
likes,
EngagementDate,
CampaignID,
ProductID,
LEFT(ViewsClicksCombined, CHARINDEX('-', ViewsClicksCombined)-1 ) as Clicks,
RIGHT(ViewsClicksCombined, LEN(ViewsClicksCombined)- CHARINDEX('-',ViewsClicksCombined)) as Views


from engagement_data

where ContentType != 'newsletter'