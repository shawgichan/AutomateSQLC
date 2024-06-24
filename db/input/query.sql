
-- name: GetAllExhibitionBooths :many 
SELECT * FROM exhibition_booths
ORDER BY id DESC 
LIMIT $1
OFFSET $2;
 
 

 
-- name: GetServiceCompanyForGraph :one 
SELECT id,
	company_name, 
	description, 
	logo_url, 
	cover_image_url, 
	is_verified, 
	commercial_license_no
FROM 
	services_companies 
WHERE 
	id=$1 
LIMIT 1;

 
-- name: GetServiceCompanyBranchForGraph :one 
SELECT id,
	company_name, 
	description, 
	logo_url, 
	cover_image_url, 
	is_verified, 
	commercial_license_no
FROM 
	service_company_branches 
WHERE 
	id=$1 
LIMIT 1;
 
 
-- name: GetDeveloperCompanyForGraph :one 
SELECT id,
	company_name, 
	description, 
	logo_url, 
	cover_image_url, 
	is_verified, 
	commercial_license_no
FROM 
	developer_companies 
WHERE 
	id=$1 
LIMIT 1;
 
 
-- name: GetDeveloperCompanyBranchForGraph :one 
SELECT id,
	company_name, 
	description, 
	logo_url, 
	cover_image_url, 
	is_verified, 
	commercial_license_no
FROM 
	developer_company_branches 
WHERE 
	id=$1 
LIMIT 1;

 
 
-- name: GetProductCompanyForGraph :one 
SELECT id,
	company_name, 
	description, 
	logo_url, 
	cover_image_url, 
	is_verified, 
	commercial_license_no
FROM 
	product_companies 
WHERE 
	id=$1 
LIMIT 1;
 
 
-- name: GetProductCompanyBranchForGraph :one 
SELECT id,
	company_name, 
	description, 
	logo_url, 
	cover_image_url, 
	is_verified, 
	commercial_license_no
FROM 
	product_companies_branches 
WHERE 
	id=$1 
LIMIT 1;