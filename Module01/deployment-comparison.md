## 1. Company scenario
# Company ABC Services.
## Requirement	Assumption
- Employees	30
- Locations	1
- IT staff	Little/no dedicated IT expertise
- Operating hours	6 days/week, 8 AM–8 PM
- IT budget	$500/month
- Applications	Employees and some customers access online applications
- Internet	Business-class Internet
- Availability	Business applications should remain available outside normal employee hours
- Growth	Small/moderate growth expected
- IT preference	Simple to administer
# 2. Compare the five choices
Option	Initial cost	Monthly infrastructure cost	Reliability	IT knowledge required	Internet/customer access	Overall fit
VirtualBox	Low	Low	Low–Medium	Medium	Possible	Development/testing
Hyper-V	Medium–High	Low–Medium	High	Medium	Yes	Good on-premises solution
Proxmox VE	Medium	Low	High	Medium–High	Yes	Technically capable
Physical PC	Low–Medium	Low	Low	Low–Medium	Possible	Simple but single point of failure
Microsoft Azure	Low upfront	Variable	High	Low–Medium	Excellent	Strong fit

## Microsoft Azure
For this particular company, Azure deserves serious consideration.
Instead of putting the production application inside the office:
The office Internet connection is no longer responsible for hosting the application.
Employees can access it from the office, while customers can access it over the Internet.
Azure provides Windows and Linux VMs, and Microsoft provides a pricing calculator for selecting and estimating VM costs
Why Azure fits this particular scenario
There are five important reasons.
## 1. The company has little IT expertise
With an on-premises server, someone has to maintain:
- Server
- Storage
- Power
- Cooling
- Networking
- Firewall
- Operating system
- Virtualization
- Backups
- Security
- Hardware

With Azure, much of the physical infrastructure is Microsoft's responsibility.
The company still has to manage the application, accounts, security configuration, backups, and cloud resources, but it doesn't have to maintain the physical server.
The $500/month budget
This is where careful architecture is important.
Don't simply purchase a large Azure VM.
Start with the smallest VM that can actually support the application and database.
Microsoft also offers reservations that can reduce VM costs when workloads have predictable long-term usage. 
The exact Azure cost cannot responsibly be determined without knowing:
-    Application type 
-  	Windows vs. Linux 
- 	CPU requirements 
- 	RAM 
- 	Database requirements 
- 	Storage 
- 	Number of simultaneous users 
- 	Internet traffic 
- 	Backup requirements

## The key design decision
I would choose Microsoft Azure for the production application, while keeping the office infrastructure simple.
The reason isn't simply that "cloud is better." It is because the combination of:
30 employees + very little IT expertise + customer Internet access + one physical location + 6-day operation + $500/month target
makes minimizing the amount of business-critical infrastructure physically located in the office particularly valuable.

