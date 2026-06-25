CREATE DATABASE `moneymate` ;
USE `moneymate` ;
CREATE TABLE students (
`student_id` int(11) NOT NULL AUTO_INCREMENT,
`username` varchar(50) NOT NULL,
`password` varchar(255) NOT NULL, 
`firstname` varchar(255) NOT NULL, 
`lastname` varchar(255) NOT NULL, 
`email` varchar(100) NOT NULL,
`school` varchar(100) NOT NULL, 
`address` varchar(100) NOT NULL, 
`city` varchar(100) NOT NULL,
`state` varchar(100) NOT NULL,
`country` varchar(100) NOT NULL,
`postalcode` varchar(100) NOT NULL, PRIMARY KEY (`student_id`)
);
select * from students;
 
CREATE TABLE transactions (
`transaction_id` int(11) NOT NULL AUTO_INCREMENT,
`student_id` int(11) NOT NULL,
`transaction_category` varchar(50) NOT NULL,
`transaction_type` varchar(50) NOT NULL,
`transaction_detail` varchar(255) NOT NULL, 
`transaction_amount` decimal(10,2) NOT NULL, 
`transaction_date` date NOT NULL,  PRIMARY KEY (`transaction_id`)
);
select * from transactions
 
select sum(total_income) as total_income, sum(total_expenses) as total_expenses, sum(total_income)-sum(total_expenses) as account_balance from (
select sum(transaction_amount) as total_income, 0 as total_expenses from transactions where transaction_category='Income'
union
select 0 as total_income, sum(transaction_amount) total_expenses from transactions where transaction_category='Expenses'
)a

