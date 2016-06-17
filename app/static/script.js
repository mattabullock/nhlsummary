$(function() {

    $.ajax({
        url:'data?gameid=2015020884'
    }).done(function(data) {
        data = JSON.parse(data);
        console.log(data);
        drawBoard(data);
    });

    var drawBoard = function(data) {
        var svg = d3.select("body")
            .append("svg")
            .attr("width", 1000)
            .attr("height", 500);
        svg.append("rect")
            .attr("cx", 25)
            .attr("cy", 25)
            .attr("rx", 75)
            .attr("ry", 75)
            .attr("width", 1000)
            .attr("height", 410)
            .style("stroke", "black")
            .style("fill", "white");
        svg.selectAll("circle")
            .data(data)
            .enter()
            .append("circle")
            .attr("cx", function (d) { return (d.event.x_coord + 100)*5; })
            .attr("cy", function (d) { return (d.event.y_coord+41)*5; })
            .attr("r", 2)
            .style("fill", function (d) {
                if(d.event.team_id === 30) {
                    return "red";
                } else {
                    return "green";
                }
            })
            .on("mouseover", mouseOver)
            .on("mouseout", mouseOut);
        drawTable(data);
    };

    var drawTable = function(d) {

        var headers = ['Player', 'Number', 'Team', 'Status'];

        // create table
        var table = d3.select('body')
            .append('table');

        // create table header
        table.append('thead').append('tr')
            .selectAll('th')
            .data(headers).enter()
            .append('th')
            .text(function(da) { return da; });

    };

    var mouseOver = function(d) {
        d3.select(this).attr("r", 5);
        console.log(d.event.event);
    };

    var mouseOut = function(d) {
        d3.select(this).attr("r", 2);
        d3.select('tbody').remove();
    };
});
