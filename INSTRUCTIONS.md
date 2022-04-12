Create an Azure PostgreSQL database
- Select "Azure Database for PostgreSQL servers" service
- Click on Create Single Server button
- Create Resource Group "dwh-group"
- Server name: divvy-db
- Location: East US
- Setup Administrator account
- Click on Review + Create button

Create an Azure Synapse workspace
- Select "Azure Synapse Analytics" service
- Select Resource Group "dwh-group"
- Workspace name: divvy-syn
- Region: East US
- Data Lake Storage Gen2:
  - Account name: divvy
  - File system name: divvyfs
- Click on Review + Create button

Create a Dedicated SQL Pool and database within the Synapse workspace
- Click on "New dedicated SQL pool"
- Pool name: divvy_pool
- Performance level: DW400c
- Click on Review + Create button

- Go to created resource "divvy-syn"
- Click on "Ingest"
- Task type: "Built-in copy task"
- Task schedule: "Run once now"
- Source Type: "Azure Database for PostgreSQL"
- Create new connection and enter properties of "divvy-db"
- Select 5 oltp tables (public.account, public.rider, public.payment, public.station, public.trip)
- Click Next
- Target Type: Azure Blob Storage
- Create new connection and enter default info
- Path: divvyfs
- Leave default fields
- Click Next
- Leave default fields
- Click Next
- Task name: CopyPipeline_divvy_oltp_v0r
- Leave default fields
- Click Next
- Validate exported data in Synapse workspace -> Linked tab -> expand "divvy-syn" -> select "divvyfs"
- Create external tables:
  - Right Click on exported file -> SQL -> Create external table -> Follow default instructions
  - Rename C1,C2,C3 columns
  - Repeat above step for each file
  - Or execute external tables sql scripts directly from `scripts/external_tables` 
- Create OLAP tables by executing sql scripts in `scripts/dwh`