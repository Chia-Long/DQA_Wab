if (!window.dash_clientside) {
    window.dash_clientside = {};
}

const baseHref = "/apps/System_Information/";
var pathName = window.location.pathname.split('/');

if (pathName[2] == "System_Information") {
	//var productName = document.getElementsByClassName("list-group-item");
	//console.log(pathName);
	document.title = pathName[3].replace("_"," ");
} else if (pathName[3] == "Frame_Loss") {
	document.title = pathName[4];
} else if (pathName[3] == "CPU_Performance" || pathName[3] == "Memory_Performance" || pathName[3] == "Storage_Performance" || pathName[3] == "LAN_Performance") {
	//console.log(pathName)
	document.title = pathName[3].replace("_"," ");
} else {
	document.title = pathName[2].replace("_"," ");
}
	
//document.title = pathName;

// create the "ui" namespace within dash_clientside
window.dash_clientside.ui = { 
    // this function should be used in the callback whenever the table viewport has changed
    replaceWithLinks: function(trigger) {
        // find all dash-table cells that are in column 0
        //let cells1 = document.getElementsByClassName("dash-header");
		//let cells1 = document.getElementsByClassName("dash-cell column-12");
		let cells1 = document.getElementsByClassName("dash-cell column-1");
		let cells2 = document.getElementsByClassName("column-header-name");
		var class_name = "dash-cell column-" + (cells2.length - 2); //取得最後一行Test_ID的Column數值
		let cells3 = document.getElementsByClassName(class_name);
		let cells4 = document.getElementsByClassName("dash-cell column-12");
		//let cells5 = document.getElementsByClassName("js-plotly-plot");
		//console.log(class_name)
		//console.log(cells2)
		//console.log(cells2[cells2.length-1])
		//console.log(cells3[0].innerText)
		//console.log(cells2)
		
        //cells1.forEach((elem, index, array) => {
        /*cells1.forEach((elem, index, array) => {
			if (elem.children[0].innerText == "Product Name" || 
				elem.children[0].innerText == "Test Date" ||
				elem.children[0].innerText == "Performance Summary" ||
				elem.children[0].innerText == "SPEC CPU® 2017" ||
				elem.children[0].innerText == "Intel® Memory Latency Checker" ||
				elem.children[0].innerText == "LAN Bandwidth" ||
				elem.children[0].innerText == "Controller" ||
				elem.children[0].innerText == "Data Rate" ||
				elem.children[0].innerText == "Port #" ||
				elem.children[0].innerText == "Detail"
				) {
				elem.children[0].innerHTML = elem.children[0].innerText;
			} else if (elem.children[0].innerText == "CPU Performance" || elem.children[0].innerText == "Memory Performance" || elem.children[0].innerText == "Storage Performance" || elem.children[0].innerText == "LAN Performance") {
				elem.children[0].innerHTML = '<a href="/apps/WebOutput/' + elem.children[0].innerText.replace(/ /g,"_") + '">' + elem.children[0].innerText + '</a>';
			//} else if (elem.children[0].innerText == "Detail") {
			//	elem.children[0].innerHTML = '<a href="/apps/WebOutput/' + elem.children[0].innerText.replace(/ /g,"_") + '">' + elem.children[0].innerText + '</a>';
			
			} else {
				elem.children[0].innerHTML =
					elem.children[0].innerText + '<a href="/apps/WebOutput/' + elem.children[0].innerText.replace(/ /g,"_") + '"><br>' + '<img align="center" src="/assets/chart.png" height="20"></a>';
					//'<a href="/apps/WebOutput/' + elem.children[0].innerText + '">' + elem.children[0].innerText + '<img align="center" //src="/assets/chart.png" height="20"></a>';
					//elem.children[0].innerText + "   " + '<a href="/apps/app3" >';
			}
            // each cell element should be modified with a new link
            // elem.children[0].innerText contains the link information, which we append to a specified route on our server
            //elem.children[0].innerHTML =
            //    '<a href="/apps/WebOutput/' + elem.children[0].innerText + '">' + elem.children[0].innerText + "</a>";
                //elem.children[0].innerText + "   " + '<a href="/apps/app3" >';
        });*/
		//console.log(cells2[0].dataset.dashColumn == "Detail");
		
		cells1.forEach((elem, index, array) => {
			//if (cells2[index].dataset.dashColumn == "Detail"){
				//elem.children[0].innerHTML = '<a href="/apps/WebOutput/Frame_Loss/' + elem.children[0].innerText + '" target="_blank">' + elem.children[0].innerText + '</a>';
				elem.children[0].innerHTML = '<a href="' + baseHref + cells3[index].innerText + '" target="_blank">' + elem.children[0].innerText + "</a>";
			//}
		});
	
		cells2.forEach((elem, index, array) => {
			if (elem.innerText == "Integer Speed(Base)" ||
				elem.innerText == "Integer Speed(Peak)" ||
				elem.innerText == "Integer Rate(Base)" ||
				elem.innerText == "Integer Rate(Peak)" ||
				elem.innerText == "Floating Point Speed(Base)" ||
				elem.innerText == "Floating Point Speed(Peak)" ||
				elem.innerText == "Floating Point Rate(Base)" ||
				elem.innerText == "Floating Point Rate(Peak)" ||
				elem.innerText == "All Reads(MB/s)" ||
				elem.innerText == "1:1 Reads Writes(MB/s)" ||
				elem.innerText == "BandWidth(MB/s)" ||
				elem.innerText == "IOPS(k)" ||
				elem.innerText == "Latency(us)" ||
				elem.innerText == "64 Bytes BW" ||
				elem.innerText == "128 Bytes BW" ||
				elem.innerText == "256 Bytes BW" ||
				elem.innerText == "512 Bytes BW" ||
				elem.innerText == "1024 Bytes BW" ||
				elem.innerText == "1280 Bytes BW" ||
				elem.innerText == "1518 Bytes BW"
			){
				//elem.children[0].innerHTML = '<a href="/apps/WebOutput/Frame_Loss/' + elem.children[0].innerText + '" target="_blank">' + elem.children[0].innerText + '</a>';
				//elem.innerHTML = '<a href="#' + elem.innerText.replace(/ /g,"_") + '">' + elem.innerText + '<img align="center" //src="/assets/chart.png" height="20"></a>' ;
				elem.innerHTML = elem.innerText + '<a href="#' + elem.innerText.replace(/ /g,"_") + '"><br><img align="center" src="/assets/poll-h-solid.svg" height="22" class="filter-bar"></a>';
				//console.log(elem.innerHTML)
			}
		});
		
		cells4.forEach((elem, index, array) => {
			if (cells4[index].dataset.dashColumn == "Detail"){
				elem.children[0].innerHTML = '<a href="/apps/WebOutput/Frame_Loss/' + elem.children[0].innerText + '" target="_blank">' + 'Link' + '</a>';
				//elem.children[0].innerHTML = '<a href="/apps/WebOutput/Frame_Loss/' + elem.children[0].innerText + '" target="_blank">' + elem.children[0].innerText + '</a>';
			}
		});
            
      	//cells3.forEach((elem, index, array) => {
            // each cell element should be modified with a new link
            // elem.children[0].innerText contains the link information, which we append to a specified route on our server
        //    elem.children[0].innerHTML =
        //        '<div style="background-color:rgb(114,163,118);width:100px;border-style:solid;border-width:2px;border-color:rgb(82,119,85);margin:5px;">' + elem.children[0].innerText;
        //});

        // arbitrary return.. callback needs a target
        return true;
    }
}


/*window.dash_clientside.bar = { 
    // this function should be used in the callback whenever the table viewport has changed
    createBarChart: function(trigger) {
        // find all dash-table cells that are in column 0
        //let cells1 = document.getElementsByClassName("dash-cell column-1");
		//let cells2 = document.getElementsByClassName("dash-cell column-2");
		//let cells3 = document.getElementsByClassName("dash-cell column-3");
		//let cells4 = document.getElementsByClassName("dash-cell column-4");
		//let cells5 = document.getElementsByTagName("a");
		//let cells6 = document.getElementsByClassName("line");
		//console.log(cells5)
		
		//console.log(test1, test2);
        //cells1.forEach((elem, index, array) => {
        //cells1.forEach((elem, index, array) => {
            // each cell element should be modified with a new link
            // elem.children[0].innerText contains the link information, which we append to a specified route on our server
        //    elem.children[0].innerHTML =
        //        '<a href="/apps/WebOutput/' + elem.children[0].innerText + '">' + elem.children[0].innerText + "</a>";
                //elem.children[0].innerText + "   " + '<a href="/apps/app3" >';
        //var Test_ID = elem.children[0].innerText;
		//console.log(Test_ID);
		//});
		
		cells2.forEach((elem, index, array) => {
            // each cell element should be modified with a new link
            // elem.children[0].innerText contains the link information, which we append to a specified route on our server
            //elem.children[0].innerHTML =
                //'<a href="/apps/app2"><img align="center" src="/assets/chart.png" height="20">';
            //    '<a href="/"><img align="center" src="/assets/chart.png" height="20">';
			//console.log(cells1[index].innerText);
			elem.children[0].innerHTML =
                '<a href="' +
                baseHref + cells1[index].innerText +
                //"systems" +
                '" target="_blank">' +
                elem.children[0].innerText +
                "</a>";
        });
		
		cells3.forEach((elem, index, array) => {
            // each cell element should be modified with a new link
            // elem.children[0].innerText contains the link information, which we append to a specified route on our server
            //elem.children[0].innerHTML =
                //'<div style="background-color:rgb(114,163,118);width:100px;border-style:solid;border-width:2px;border-color:rgb(82,119,85);margin:5px;"><p>100</p>';
            //    '<div style="background-color:rgb(114,163,118);width:' + elem.children[0].innerText + 'px;border-style:solid;border-width:2px;border-color:rgb(82,119,85);margin:5px;">' + elem.children[0].innerText;
			elem.children[0].innerHTML =
                //'<div style="background-color:rgb(114,163,118);width:100px;border-style:solid;border-width:2px;border-color:rgb(82,119,85);margin:5px;"><p>100</p>';
                '<div style="background-color:rgb(114,163,118);width:' + cells4[index].innerText + '%;border-style:solid;border-width:2px;border-color:rgb(82,119,85);margin:5px">' + elem.children[0].innerText;
        
        });

        // arbitrary return.. callback needs a target
        return true;
    }
}
*/

window.dash_clientside.storage = { 
    // this function should be used in the callback whenever the table viewport has changed
    mergeTableRow: function(trigger) {
        // find all dash-table cells that are in column 0
        //let cells1 = document.getElementsByClassName("dash-header");
		let cells1 = document.getElementsByClassName("column-header-name");
		let cells2 = document.getElementsByClassName("dash-header");
		let cells3 = document.getElementsByClassName("dash-header column-2");
		let cells4 = document.getElementsByClassName("dash-cell column-0");
		let cells5 = document.getElementsByClassName("dash-cell column-2");
		//let cells4 = document.getElementsByClassName("dash-header column-17");
		//let cells4 = document.getElementsByClassName("dash-header column-3");
		//let cells5 = document.getElementsByClassName("dash-header column-4");
		//console.log(cells4[1])
		//console.log(cells1[11].parentNode.parentNode.getAttributeNode("data-dash-column"));
		//cells4[0].remove();
		//cells4[0].remove();
		//console.log(cells5[0].dataset.dashColumn)
		//cells2[1].rowSpan = "2";
		//cells2[2].remove();
		//cells3[0].rowSpan = "2";
		//cells3[1].remove();
		console.log(cells2)
		cells1.forEach((elem, index, array) => {
			if (elem.innerText == "BandWidth (MB/s)" ||
				elem.innerText == "IOPS (k)" ||
				elem.innerText == "Latency (us)"
			){
				//elem.children[0].innerHTML = '<a href="/apps/WebOutput/Frame_Loss/' + elem.children[0].innerText + '" target="_blank">' + elem.children[0].innerText + '</a>';
				//elem.innerHTML = '<a href="#' + elem.innerText.replace(/ /g,"_") + '">' + elem.innerText + '<img align="center" //src="/assets/chart.png" height="20"></a>' ;
				//console.log(cells1[index].parentNode.parentNode.getAttributeNode("data-dash-column").value)
				elem.innerHTML = elem.innerText + '<a href="#' + cells1[index].parentNode.parentNode.getAttributeNode("data-dash-column").value + '"><br><img align="center" src="/assets/poll-h-solid.svg" height="22" class="filter-bar"></a>';
				//console.log(elem.innerHTML)
			}
		});
		
		cells5.forEach((elem, index, array) => {
			//if (cells2[index].dataset.dashColumn == "Detail"){
				//elem.children[0].innerHTML = '<a href="/apps/WebOutput/Frame_Loss/' + elem.children[0].innerText + '" target="_blank">' + elem.children[0].innerText + '</a>';
				elem.children[0].innerHTML = '<a href="' + baseHref + cells4[index].innerText + '" target="_blank">' + elem.children[0].innerText + "</a>";
			//}
		});
		/*
		cells1.forEach((elem, index, array) => {
			if (elem.children[0].innerText == "BandWidth(MB/s)" || 
			    elem.children[0].innerText == "IOPS(k)" ||
				elem.children[0].innerText == "Latency(us)"
				){
				elem.children[0].innerHTML =
					elem.children[0].innerText + '<a href="/apps/WebOutput/' + cells1[index].dataset.dashColumn + '"><br>' + '<img align="center" src="/assets/chart.png" height="20"></a>';
			} else {
				elem.children[0].innerHTML = elem.children[0].innerText;
			}
            // each cell element should be modified with a new link
            // elem.children[0].innerText contains the link information, which we append to a specified route on our server
            //elem.children[0].innerHTML =
            //    '<a href="/apps/WebOutput/' + elem.children[0].innerText + '">' + elem.children[0].innerText + "</a>";
                //elem.children[0].innerText + "   " + '<a href="/apps/app3" >';
        });*/
		
		//cells2.forEach((elem, index, array) => {
            // each cell element should be modified with a new link
            // elem.children[0].innerText contains the link information, which we append to a specified route on our server
            //elem.children[0].innerHTML =
                //'<a href="/apps/app2"><img align="center" src="/assets/chart.png" height="20">';
            //    '<a href="/"><img align="center" src="/assets/chart.png" height="20">';
			//console.log(cells1[index].innerText);
			//elem.children[0].innerHTML =
            //    '<a href="' +
            //    baseHref + cells1[index].innerText +
            //    //"systems" +
            //    '" target="_blank">' +
            //    elem.children[0].innerText +
            //    "</a>";
        //});

        // arbitrary return.. callback needs a target
        return true;
    }
}