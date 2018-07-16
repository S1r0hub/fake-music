// REQUIRES d3js
// Get it here: https://github.com/d3/d3
// (c) github.com/S1r0hub


function LossGraph(data) {

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

      // set the ranges
      var x = this.x
      var y = this.y

      // Get the data domain
      this.x.domain(d3.extent(data, function(d) { return d.epoch; }));
      this.y.domain([0, Math.ceil(d3.max(data, function(d) { return d.loss; }))]);

      // clear current svg
      this.svg.selectAll("*").remove();

      // add the x axis
      this.svg.append("g")
         .call(d3.axisBottom(this.x))
         .attr("transform", "translate(0," + this.height + ")")

      // x-label
      this.svg.append("text")
         .attr(
            "transform",
            "translate(" + (this.width / 2) + " ," + (this.height + this.margin.top + 5) + ")")
         .style("text-anchor", "middle")
         .style("font-size", "12px")
         .style("fill", "steelblue")
         .text("Epoch");

      // add the y axis
      this.svg.append("g")
         .call(d3.axisLeft(this.y));

      // y-label
      this.svg.append("text")
         .attr("fill", "#000")
         //.attr("transform", "rotate(-90)")
         .attr("y", -15)
         .attr("dy", "0em")
         .attr("text-anchor", "end")
         .style("font-size", "12px")
         .style("fill", "steelblue")
         .text("Loss");

      // add the path
      this.svg.append("path")
         .data([data])
         .attr("fill", "none")
         .attr("stroke", "steelblue")
         .attr("stroke-width", 2)
         .attr("d", this.line);

      // focus for mouse over
      // original code by: https://bl.ocks.org/mbostock/3902569
      var focus = this.svg.append("g")
         .attr("class", "focus")
         .style("display", "none");

      focus.append("circle")
         .attr("r", 4);

      focus.append("text")
         .attr("dx", "-1.5em")
         .attr("dy", "-1.0em");

      this.svg.append("rect")
         .attr("class", "overlay")
         .attr("width", this.width)
         .attr("height", this.height)
         .on("mouseover", function() { focus.style("display", null); })
         .on("mouseout", function() { focus.style("display", "none"); })
         .on("mousemove", mousemove);

      function mousemove() {
         var i = Math.round(x.invert(d3.mouse(this)[0]));
         var d = data[i];
         focus.attr("transform", "translate(" + x(d.epoch) + "," + y(d.loss) + ")");
         focus.select("text").text(d.loss);
      }
   }

   this.sizeUpdate = function(width_in, height_in) {

      // set the dimensions and margins of the graph
      this.margin = {top: 30, right: 50, bottom: 45, left: 25};
      this.width = width_in - this.margin.left - this.margin.right;

      if (height_in) {
         this.height = height_in - this.margin.top - this.margin.bottom;
      }

      // set the ranges
      this.x = d3.scaleLinear().rangeRound([0, this.width]);
      this.y = d3.scaleLinear().rangeRound([this.height, 0]);
      var x = this.x;
      var y = this.y;

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

      this.update();
   }

   // perform initial size update
   this.sizeUpdate(800, 200);
}
