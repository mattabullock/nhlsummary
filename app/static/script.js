$(function() {

    $.ajax({
        url:'data'
    }).done(function(data) {
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
            .attr("rx", 100)
            .attr("ry", 100)
            .attr("width", 1000)
            .attr("height", 500)
            .style("stroke", "black")
            .style("fill", "white");
        svg.append("circle")
            .attr("cx", 25)
            .attr("cy", 25)
            .attr("r", 25)
            .style("fill", "purple");
    };
});
