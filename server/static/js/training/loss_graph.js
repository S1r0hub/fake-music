// REQUIRES d3js
// Get it here: https://github.com/d3/d3
// (c) github.com/S1r0hub


function LossGraph(data) {

   // set the dimensions and margins of the graph
   this.margin = {top: 0, right: 1, bottom: 20, left: 25};
   this.width = 800 - this.margin.left - this.margin.right;
   this.height = 200 - this.margin.top - this.margin.bottom;

   // set the ranges
   var x = d3.scaleLinear().rangeRound([0, this.width]);
   this.x = x;
   var y = d3.scaleLinear().rangeRound([this.height, 0]);
   this.y = y;

   // create info how to build the graph line
   this.line = d3.line()
      .x(function(d) { return x(d.epoch); })
      .y(function(d) { return y(d.loss); });

   // append the svg obgect to the div
   this.maindiv = d3.select("#loss-graph");
   this.maindiv.selectAll("svg").remove(); // remove all svgs
   this.svg = this.maindiv.append("svg")
      .attr("width", this.width + this.margin.left + this.margin.right)
      .attr("height", this.height + this.margin.top + this.margin.bottom)
      .append("g").attr(
         "transform",
         "translate(" + this.margin.left + "," + this.margin.top + ")"
      );

   // the actual data
   this.data = data;

   // get currently used data
   this.get_data = function() {
      return this.data;
   }

   // update the graph
   this.update = function(data) {

      // store new data
      if (!data) { data = this.data; }
      else { this.data = data; }

      // Get the data domain
      this.x.domain(d3.extent(data, function(d) { return d.epoch; }));
      this.y.domain([0, d3.max(data, function(d) { return d.loss; })]);

      // clear current svg
      this.svg.selectAll("*").remove();

      // Add the X Axis
      this.svg.append("g")
         .attr("transform", "translate(0," + this.height + ")")
         .call(d3.axisBottom(this.x));

      // Add the Y Axis
      this.svg.append("g")
         .call(d3.axisLeft(this.y))
         .append("text")
            .attr("fill", "#000")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", "0.71em")
            .attr("text-anchor", "end")
            .text("Loss");

      // Add the path
      this.svg.append("path")
         .data([data])
         .attr("fill", "none")
         .attr("stroke", "steelblue")
         .attr("stroke-width", 2)
         .attr("d", this.line);
   }
}
