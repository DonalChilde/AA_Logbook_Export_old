<?xml version = "1.0" encoding = "UTF-8"?>
<!-- xsl stylesheet declaration with xsl namespace: 
Namespace tells the xlst processor about which 
element is to be processed and which is used for output purpose only 
-->
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"> 
<!-- xsl template declaration:  
template tells the xlst processor about the section of xml 
document which is to be formatted. It takes an XPath expression. 
In our case, it is matching document root element and will 
tell processor to process the entire document with this template. 
-->
<xsl:template match="/"> 
<html>
<head>
	<style type="text/css">
            body{
                font-family: sans-serif;
                font-weight:300;
                padding-top:30px;
                color:#666;
            }
            .container{
                text-align:center;  
            }
            a{ color:#1C2045; font-weight:350;}
            table{
                font-weight:300;
                margin:0px auto;
                border: 1px solid #1C2045;
                padding:5px;
                color:#666;

            }
            th,td{ 
                border-bottom: 1px solid #dddddd;
                text-align:center;
                margin: 10px;
                padding:0 10px;
            }
            hr{ 
                border:0;
                border-top: 1px solid #E7C254;
                margin:20px auto;
                width:50%;
            }
            .button{
                background-color:#1C2045;
                color:#E7C254;
                padding:5px 20px;
                max-width: 300px;
                line-height:1.5em;
                text-align:center;
                margin:5px auto;
            }
            .button a{ color:#E7C254;}
            .refs{ display:block; margin:auto; text-align:left; max-width:500px; }
            .refs .label{  font-size:1.4em;}
            .refs > ul{ margin-top:10px; line-height:1.5em;}
        </style>
	<title> Exporting APA Logbook Data to a CSV File </title>
</head>
<body>
<div class='container'>
	<div id="dvData">
		<table>
			<tr>
				<th> Sequence Number </th>
				<th> POS </th>
				<th> TYPE </th>
				<th> IDENT </th>
				<th> MDL </th>
				<th> EQ </th>
				<th> FLT </th>
				<th> DEPT STA </th>
				<th> DEP TIME </th>
				<th> DEP +- </th>
				<th> ARR STA </th>
				<th> ARR TIME </th>
				<th> ARR +- </th>
				<th> FLY </th>
				<th> GTR </th>
				<th> BLOCK </th>
				<th> GRD </th>
				<th> ODL </th>
				<th> FUEL +- </th>
				<th> DELAY </th>
			</tr>
			<xsl:for-each select="CrystalReport/Group[@Level='1']"> <xsl:for-each select="Group[@Level='2']"> <xsl:for-each select="Group[@Level='3']"> <xsl:variable name="sequencenumber" select="GroupHeader/Section/Text[@Name='Text10']/TextValue" /> <xsl:for-each select="Group[@Level='4']"> <xsl:for-each select="Details/Section"> 
			<tr>
				<td> <xsl:value-of select="$sequencenumber" /> </td>
				<td> <xsl:value-of select="Field[@Name='ActulaPos1']/Value" /> </td>
				<td> <xsl:value-of select="Field[@Name='EQType1']/Value" /> </td>
				<td> <xsl:value-of select="Field[@Name='AcNum1']/Value" /> </td>
				<td> <xsl:value-of select="Field[@Name='Model1']/Value" /> </td>
				<td> <xsl:value-of select="Field[@Name='LeqEq1']/Value" /> </td>
				<td> <xsl:value-of select="Field[@Name='Flt1']/Value" /> </td>
				<td> <xsl:value-of select="Field[@Name='DepSta1']/Value" /> </td>
				<td> <xsl:value-of select="Field[@Name='OutDtTime1']/Value" /> </td>
				<td> <xsl:value-of select="Field[@Name='DepPerf1']/Value" /> </td>
				<td> <xsl:value-of select="Field[@Name='ArrSta1']/Value" /> </td>
				<td> <xsl:value-of select="Field[@Name='InDateTimeOrMins1']/Value" /> </td>
				<td> <xsl:value-of select="Field[@Name='ArrPerf1']/Value" /> </td>
				<td> <xsl:value-of select="Field[@Name='Fly1']/Value" /> </td>
				<td> <xsl:value-of select="Field[@Name='LegGtr1']/Value" /> </td>
				<td> <xsl:value-of select="Field[@Name='ActualBlock1']/Value" /> </td>
				<td> <xsl:value-of select="Field[@Name='Grd1']/Value" /> </td>
				<td> <xsl:value-of select="Field[@Name='DpActOdl1']/Value" /> </td>
				<td> <xsl:value-of select="Field[@Name='FuelPerf1']/Value" /> </td>
				<td> <xsl:value-of select="Field[@Name='DlyCode1']/Value" /> </td>
			</tr>
			</xsl:for-each> </xsl:for-each> </xsl:for-each> </xsl:for-each> </xsl:for-each> 
		</table>
	</div>
	<br />
	<div class='button'>
		<a href="#" id="export" role='button'> Click On This Here Link To Export The Table Data into a CSV File </a> 
	</div>
	<hr />
	<div class='refs'>
		<div class='label'>
			References 
		</div>
		<ul>
			<li> <a href="http://stackoverflow.com/questions/16078544/export-to-csv-using-jquery-and-html" target="_blank"> Export to CSV using jQuery and HTML (Stack Overflow) </a> </li>
			<li> <a href="http://adilapapaya.wordpress.com/2013/11/15/exporting-data-from-a-web-browser-to-a-csv-file-using-javascript/" target="_blank"> adilapapaya.wordpress.com </a> </li>
		</ul>
	</div>
	<hr />
</div>
</body>
<script type='text/javascript' src='https://code.jquery.com/jquery-2.1.0.min.js'>
</script>

<!-- If you want to use jquery 2+: https://code.jquery.com/jquery-2.1.0.min.js -->
<script type='text/javascript'>

        $(document).ready(function () {

            console.log("HELLO")
            function exportTableToCSV($table, filename) {
                var $headers = $table.find('tr:has(th)')
                    ,$rows = $table.find('tr:has(td)')

                    // Temporary delimiter characters unlikely to be typed by keyboard
                    // This is to avoid accidentally splitting the actual contents
                    ,tmpColDelim = String.fromCharCode(11) // vertical tab character
                    ,tmpRowDelim = String.fromCharCode(0) // null character

                    // actual delimiter characters for CSV format
                    ,colDelim = '","'
                    ,rowDelim = '"\r\n"';

                    // Grab text from table into CSV formatted string
                    var csv = '"';
                    csv += formatRows($headers.map(grabRow));
                    csv += rowDelim;
                    csv += formatRows($rows.map(grabRow)) + '"';

                    // Data URI
                    var csvData = 'data:application/csv;charset=utf-8,' + encodeURIComponent(csv);

                $(this)
                    .attr({
                    'download': filename
                        ,'href': csvData
                        //,'target' : '_blank' //if you want it to open in a new window
                });

                //------------------------------------------------------------
                // Helper Functions 
                //------------------------------------------------------------
                // Format the output so it has the appropriate delimiters
                function formatRows(rows){
                    return rows.get().join(tmpRowDelim)
                        .split(tmpRowDelim).join(rowDelim)
                        .split(tmpColDelim).join(colDelim);
                }
                // Grab and format a row from the table
                function grabRow(i,row){
                     
                    var $row = $(row);
                    //for some reason $cols = $row.find('td') || $row.find('th') won't work...
                    var $cols = $row.find('td'); 
                    if(!$cols.length) $cols = $row.find('th');  

                    return $cols.map(grabCol)
                                .get().join(tmpColDelim);
                }
                // Grab and format a column from the table 
                function grabCol(j,col){
                    var $col = $(col),
                        $text = $col.text();

                    return $text.replace('"', '""'); // escape double quotes

                }
            }


            // This must be a hyperlink
            $("#export").click(function (event) {
                // var outputFile = 'export'
                var outputFile = window.prompt("What do you want to name your output file (Note: This won't have any effect on Safari)") || 'export';
                outputFile = outputFile.replace('.csv','') + '.csv'
                 
                // CSV
                exportTableToCSV.apply(this, [$('#dvData>table'), outputFile]);
                
                // IF CSV, don't do event.preventDefault() or return false
                // We actually need this to be a typical hyperlink
            });
        });
    
</script>
</html>
</xsl:template> </xsl:stylesheet> 