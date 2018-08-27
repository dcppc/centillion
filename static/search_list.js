//////////////////////////////////
// Centillion Search Results Listing
// Javascript Functions 
//
// This file contains javascript functions used by
// the search results page centillion.



//////////////////////////////////
// Results-to-DataTable Functions
//
// These functions post-process the table of search results
// and make it into a dataTable.
//
// The dataTable bootstrap plugin is used to make the tables
// sortable, searchable, and slick.


$(document).ready(function() {
    // Construct names of id tags
    table_id = "#search-results";

    // Initialize the DataTable
    $(table_id).DataTable({
        responsive: true,
        searching: false,
        order: [[0,'desc']],
        aoColumnDefs: [
            { bSortable: false,
              aTargets : [2]
            }
        ],
        lengthMenu: [10,20,50,100]
    });

    console.log('Finished loading search results list');
});

