# editablegrid-python-sqlite-example
This example shows how to use EditableGrid with Python/Flask as a WebFramework and a SQLite database. The example is based on 
[editablegrid-mysql-example](https://github.com/webismymind/editablegrid-mysql-example) writen originally in php by 
[webismymind](https://github.com/webismymind). All php files where converted to python and javascript files kept to their 
original content except with demo.js.

The same copyrights apply to this code that was applied to the original code.

## Installation

You can load index.html in a browser and you should see the content of the table demo.

##Load data
EditableGrid supports two types of data : JSON and XML. In this example, we use JSON : 

	$grid->renderJSON($result);  

But this works too : 
	
	$grid->renderXML($result); 

Be careful to use the appropriate function in the Javascript.
JSON : 

	DatabaseGrid.prototype.fetchGrid = function()  {
	// call a PHP script to get the data
		this.editableGrid.loadJSON("loaddata.php?db_tablename=demo");
	};

XML :

	DatabaseGrid.prototype.fetchGrid = function()  {
	// call a PHP script to get the data
	this.editableGrid.loadXML("loaddata.php?db_tablename=demo");
	};


## Filter
### Client side
It's very easy to filter the content of the table. You can use

	EditableGrid.prototype.filter = function(filterString, cols)
	
In this example, the filter operates on all columns 
	
	datagrid.editableGrid.filter( $(this).val());

but you can filter only on some columns. Below, the filter operates on columns 0, 3 and 5. 

	datagrid.editableGrid.filter( $(this).val(), [0,3,5]);
	
### Server side
Coming...

	
## Pagination
### Client sid
Step to add a paginator

* Add a div to render the paginator
       
    ```
   <!-- Paginator control -->
   <div id="paginator"></div>
   ```

* In the constructor, define the pageSize and call the method that renders the paginator, once the table is rendererd.

     ```
  // define the number of row visible by page
      	pageSize: 10,
      // Once the table is displayed, we update the paginator state
        tableRendered:  function() {  updatePaginator(this); },
  ```
* The method updatePaginator builds and renders the paginator.





### Server side
Coming...	
	


## CRUD Actions 
A column **action** (type HTML) has been added. With a renderer, the content is redefined to add icons or any components to manage actions on the row

### Delete
The delete fonction calls **delete.php** with the tablename and the row id. The script executes the query that deletes the row and returns a status. If it's ok, we remove the row from the javascript model : 

	if (response == "ok" )
		        self.editableGrid.removeRow(id);
	
### Add
By clicking on the add button, a form is shown to enter a name and a firstname. 
Data are sent to add.php that executes the insert query and returns the status of the operation. 


## Responsive
This example uses the first technique describes here http://elvery.net/demo/responsive-tables/. This technique is very simple, it hide less important columns on smaller screen sizes.
	
