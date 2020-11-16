
// Calculate y interval based on year range.
// and x interval based on the number of paper in each year
function getNodes(paper_data, width, height) {
    var node = paper_data.nodes;
    var year_max = node[0].year; 
    var year_min = node[node.length-1].year; 
    var year_cnt = [0];
    var current_year = year_max;
    var year_idx = 0;
    for (var i=0; i<node.length; i++) {
        if (current_year == node[i].year) {
        } else {
            year_cnt.push(0);
            year_idx++;
            current_year = node[i].year;
        } 
        year_cnt[year_idx]++; 
    }
    var year_idx = 0;
    var node_idx = 0;
    for (var i=0; i<year_cnt.length; i++) {
        for (var j=0; j<year_cnt[i]; j++) {
            node[node_idx].x = parseInt((j + 1)/ (year_cnt[i] +1) * width, 10);
            node[node_idx].y = parseInt((node[node_idx].year - year_min + 1)/ (year_max - year_min +2) * height, 10);
            node_idx++;
        }
    }
    return node;
} 

// Find node corresponding to id
function findNode(nodes, id) {
    for (var i in nodes) {
        if ( nodes[i].id == id ) {
            return nodes[i];
        }
    }
    return [];
}
         
function getLinks(paper_data, nodes) {
    var links_data = paper_data.links;
    var links =[];
    for (var i=0; i<links_data.length;i++) {
        links.push({'source': findNode(nodes,links_data[i].from), 'target': findNode(nodes,links_data[i].to)});
    }
    //console.log(links);
    return links;
}
function setHighlight(thisNode) {
    var link = svg.selectAll("path.link")
        .attr("stroke", function(d) {
            return (d.source.id == thisNode.id || d.target.id == thisNode.id) ? "red": "blue";
        })

}

//    for (var i=0; i<links_data.length;i++
