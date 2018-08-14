var gdoc_table = false;
var issue_table = false;
var ghfile_table = false;
var markdown_table = false;

function load_gdoc_table(){
    var divList = $('div#collapseDrive').attr('class');
    if (divList.indexOf('in') !== -1) {
        console.log('Closing Google Drive master list');
    } else { 
        console.log('Opening Google Drive master list');

        $.getJSON("/list/gdoc", function(result){

            if(!gdoc_table) {
                var r = new Array(), j = -1, size=result.length;
                r[++j] = '<thead>'
                r[++j] = '<tr class="header-row">';
                r[++j] = '<th width="50%">File Name</th>';
                r[++j] = '<th width="30%">Owner</th>';
                r[++j] = '<th width="20%">Type</th>';
                r[++j] = '</tr>';
                r[++j] = '</thead>'
                r[++j] = '<tbody>'
                for (var i=0; i<size; i++){
                    r[++j] = '<tr><td>';
                    r[++j] = '<a href="' + result[i]['url'] + '" target="_blank">'
                    r[++j] = result[i]['title'];
                    r[++j] = '</a>'
                    r[++j] = '</td><td>';
                    r[++j] = result[i]['owner_name'];
                    r[++j] = '</td><td>';
                    r[++j] = result[i]['mimetype'];
                    r[++j] = '</td></tr>';
                }
                r[++j] = '</tbody>'
                $('#gdocs-master-list').html(r.join(''));
                $('#gdocs-master-list').DataTable({
                    responsive: true,
                    lengthMenu: [50,100,250,500]
                });
                gdoc_table = true;
            }
        });
        console.log('Finished loading Google Drive master list');
    }
}

function load_issue_table(){
    var divList = $('div#collapseIssues').attr('class');
    if (divList.indexOf('in') !== -1) {
        console.log('Closing Github issues master list');
    } else { 
        console.log('Opening Github issues master list');

        $.getJSON("/list/issue", function(result){
            if(!issue_table) {
                var r = new Array(), j = -1, size=result.length;
                r[++j] = '<thead>'
                r[++j] = '<tr class="header-row">';
                r[++j] = '<th width="70%">Issue Name</th>';
                r[++j] = '<th width="30%">Repository</th>';
                r[++j] = '</tr>';
                r[++j] = '</thead>'
                r[++j] = '<tbody>'
                for (var i=0; i<size; i++){
                    r[++j] ='<tr><td>';
                    r[++j] = '<a href="' + result[i]['url'] + '" target="_blank">'
                    r[++j] = result[i]['title'];
                    r[++j] = '</a>'
                    r[++j] = '</td><td>';
                    r[++j] = '<a href="' + result[i]['repo_url'] + '" target="_blank">'
                    r[++j] = result[i]['repo_name'];
                    r[++j] = '</a>'
                    r[++j] = '</td></tr>';
                }
                r[++j] = '</tbody>'
                $('#issues-master-list').html(r.join(''));
                $('#issues-master-list').DataTable({
                    responsive: true,
                    lengthMenu: [50,100,250,500]
                });
                issues_table = true;
            }
        });
        console.log('Finished loading Github issues master list');
    }
}

function load_ghfile_table(){
    var divList = $('div#collapseFiles').attr('class');
    if (divList.indexOf('in') !== -1) {
        console.log('Closing Github files master list');
    } else { 
        console.log('Opening Github files master list');

        $.getJSON("/list/ghfile", function(result){
            if(!ghfile_table) {
                console.log("-----------");
                console.log(result);
                var r = new Array(), j = -1, size=result.length;
                r[++j] = '<thead>'
                r[++j] = '<tr class="header-row">';
                r[++j] = '<th width="70%">File Name</th>';
                r[++j] = '<th width="30%">Repository</th>';
                r[++j] = '</tr>';
                r[++j] = '</thead>'
                r[++j] = '<tbody>'
                for (var i=0; i<size; i++){
                    r[++j] ='<tr><td>';
                    r[++j] = '<a href="' + result[i]['url'] + '" target="_blank">'
                    r[++j] = result[i]['title'];
                    r[++j] = '</a>'
                    r[++j] = '</td><td>';
                    r[++j] = '<a href="' + result[i]['repo_url'] + '" target="_blank">'
                    r[++j] = result[i]['repo_name'];
                    r[++j] = '</a>'
                    r[++j] = '</td></tr>';
                }
                r[++j] = '</tbody>'
                $('#ghfiles-master-list').html(r.join(''));
                $('#ghfiles-master-list').DataTable({
                    responsive: true,
                    lengthMenu: [50,100,250,500]
                });
                ghfile_table = true;
            }
        });
        console.log('Finished loading Github file list');
    }
}

function load_markdown_table(){
    var divList = $('div#collapseMarkdown').attr('class');
    if (divList.indexOf('in') !== -1) {
        console.log('Closing Github markdown master list');
    } else { 
        console.log('Opening Github markdown master list');

        $.getJSON("/list/markdown", function(result){
            if(!markdown_table) {
                var r = new Array(), j = -1, size=result.length;
                r[++j] = '<thead>'
                r[++j] = '<tr class="header-row">';
                r[++j] = '<th width="70%">Markdown File Name</th>';
                r[++j] = '<th width="30%">Repo</th>';
                r[++j] = '</tr>';
                r[++j] = '</thead>'
                r[++j] = '<tbody>'
                for (var i=0; i<size; i++){
                    r[++j] ='<tr><td>';
                    r[++j] = '<a href="' + result[i]['url'] + '" target="_blank">'
                    r[++j] = result[i]['title'];
                    r[++j] = '</a>'
                    r[++j] = '</td><td>';
                    r[++j] = '<a href="' + result[i]['repo_url'] + '" target="_blank">'
                    r[++j] = result[i]['repo_name'];
                    r[++j] = '</a>'
                    r[++j] = '</td></tr>';
                }
                r[++j] = '</tbody>'
                $('#markdown-master-list').html(r.join(''));
                $('#markdown-master-list').DataTable({
                    responsive: true,
                    lengthMenu: [50,100,250,500]
                });
                markdown_table = true;
            }
        });
        console.log('Finished loading Markdown list');
    }
}

