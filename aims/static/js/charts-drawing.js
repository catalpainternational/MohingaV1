
var global_legend_v_gap = 5;
var global_legend_box_width = 30;
var global_legend_box_height = 12;

function default_click(){}

var abs = Math.abs;
var d3_formatPrefixes = [ "y", "z", "a", "f", "p", "n", "µ", "m", "", "K", "M", "B", "T", "P", "E", "Z", "Y" ].map(d3_formatPrefix);
  d3.formatPrefix = function(value, precision) {
    var i = 0;
    if (value) {
      if (value < 0) value *= -1;
      if (precision) value = d3.round(value, d3_format_precision(value, precision));
      i = 1 + Math.floor(1e-12 + Math.log(value) / Math.LN10);
      i = Math.max(-24, Math.min(24, Math.floor((i <= 0 ? i + 1 : i - 1) / 3) * 3));
    }
    return d3_formatPrefixes[8 + i / 3];
  };
function d3_formatPrefix(d, i) {
    var k = Math.pow(10, abs(8 - i) * 3);
    return {
      scale: i > 8 ? function(d) {
        return d / k;
      } : function(d) {
        return d * k;
      },
      symbol: d
    };
  }

function draw_bar_chart_into_div(parent_id, data, width, height, margins, click, special_one, tooltip, text_above, format_tooltip) {
    if (data.length == 0){
        no_data_bar_chart(parent_id, width, height);
        return;
    }
    height = height - margins.top - margins.bottom;
    if (click == '' || click == undefined){
        click=default_click;
    }
    var x = d3.scale.ordinal()
        .rangeRoundBands([0, width-margins.left-margins.right], .1);

    var y = d3.scale.linear()
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .tickFormat(d3.format('s'))
        .orient("left");

    var chart = d3.select(parent_id).append("svg")
        .attr("width", width)
        .attr("height", height + margins.top + margins.bottom)
        .append("g")
        .attr("transform", "translate(" + margins.left + "," + margins.top + ")");

    x.domain(data.map(function (d) {
        return d.name;
    }));
    y.domain([0, d3.max(data, function (d) {
        return d.value;
    })]);
    

    chart.selectAll(".bar")
        .data(data)
        .enter().append("rect")
        .attr("class", function (d){
            var class_name = "bar "+d.code;
            if (special_one != undefined  && special_one == d.code){
                class_name += " highlighted";
            }
            return class_name;
        })
        .attr("x", function (d) {
            return x(d.name);
        })
        
        .attr("y", function (d) {
            return y(d.value);
        })
        .attr("height", function (d) {
            return height - y(d.value)
        })
        .attr("width", x.rangeBand())
        .on('click', click);
//        .attr("height", bar_height)
//        .transition()
//        .ease("elastic")
//        .delay(200)
//        .duration(3000)
//        .attr("height", function (d){return y(d.value);
//        
//        }); 



    // LEGEND
    var legend_align = "end";
    var y_translate = height;
    if (text_above == true){
        legend_align = "start";
        y_translate = y_translate -  margins.top - 5; //margins.bottom -
    }

    chart.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0, "+y_translate+")")
        .call(xAxis)
        .selectAll("text")
        .data(data)
        .style("text-anchor", legend_align)
        .attr("class", "legend_x_axis")
        .attr("dx", "-.8em")
        .attr("dy", "-.6em")
        .attr("transform", function (d) {
            return "rotate(-90)"
        })
        .on('click', click);

    chart.append("g")
        .attr("class", "y axis")
        .call(yAxis);

    var default_tooltips = function() 
    {
        var d = this.__data__;
        return d.name + "<br>$"+ d.pretty;
    };

    var xAxisTooltip = function()
    {
        var d = data;
        var currentObject = this.__data__;
        var title;
        if ( format_tooltip )
            title = format_tooltip({'name': currentObject.name, 'value': currentObject.pretty});
        else
            title = currentObject.name + '<br>' + currentObject.pretty;

        return title;
    };

    if (!tooltip){
        tooltip = default_tooltips;
    }

    $('svg rect, svg text.name, svg text.score').tipsy({
        gravity: 's',
        html: true,
        title: tooltip
      });

    $('svg text.legend_x_axis').tipsy({
        gravity: 's',
        html: true,
        delayIn: 5,
        title: xAxisTooltip
      });

    function type(d) {
        d.value = +d.value; // coerce to number
        return d;
    }
}

function draw_horizontal_bar_chart_into_div(parent_id, data, width, bar_height, count_tooltip){
    if (data.length == 0){
        no_data_bar_chart(parent_id, width, bar_height* 6);
        return;
    }
    var chart,
        height = bar_height * data.length;

    var x, y;

    x = d3.scale.linear()
        .domain([0, d3.max(data, function (d) {return d.value;})])
        .range([0, width]);

    var left_width = 0;

    var gap = 2;
    y = d3.scale.ordinal()
        .domain(data.map(function(d,i){return i;}))//data.map(function(d){return d.name;}))
        .rangeBands([0, (bar_height + 2 * gap) * data.length]);

    chart = d3.select(parent_id)
        .append('svg')
        .attr('class', 'chart')
        .attr('width', left_width + width)
        .attr('height', (bar_height + gap * 2) * data.length + 30)
        .append("g")

    chart.selectAll("rect")
        .data(data)
        .enter().append("rect")
        .attr("x", left_width)
        .attr("y", function(d,i) { return y(i) + gap; })
        .attr("width", 0)
        .attr("height", bar_height)
        .transition()
        .ease("elastic")
        .delay(200)
        .duration(3000)
        .attr("width", function (d){return x(d.value);});        

    chart.selectAll("text.score")
        .data(data)
        .enter().append("text")
        .attr("x", width)
        .attr("y", function(d, i){ return y(i) + y.rangeBand()/2; } )
        .attr("dx", -5)
        .attr("dy", ".30em")
        .attr("text-anchor", "end")
        .attr('class', 'score')
        .text(function(d){return "$"+d.pretty;});
        

    chart.selectAll("text.name")
        .data(data)
        .enter().append("text")
        .attr("x", left_width / 2)
        .attr("y", function(d, i){ return y(i) + y.rangeBand()/2;})
        .attr("dy", ".32em")
        .attr("dx", ".65em")
        .attr('class', 'name')
        .text(function(d){return d.name;})
        .call(wrap , width-70);

    if(count_tooltip){
        console.log('tooltip on horizontal');
        $('svg text.name').tipsy({
        gravity: 's',
        html: true,
        title: count_tooltip

      });
    }
}

function draw_horizontal_bar_chart_into_div_selectable(parent_id, data, width, bar_height, click, special_one,  count_tooltip){
    if (data.length == 0){
        no_data_bar_chart(parent_id, width, bar_height * 6);
        return;
    }
    if (click == '' || click == undefined){
        click=default_click;
    }
    var chart,
        height = bar_height * data.length;

    var x, y;

    x = d3.scale.linear()
        .domain([0, d3.max(data, function (d) {return d.value;})])
        .range([0, width]);

    var left_width = 0;

    var gap = .7;
    y = d3.scale.ordinal()
        .domain(data.map(function(d,i){return i;}))//data.map(function(d){return d.name;}))
        .rangeBands([0, (bar_height + 2 * gap) * data.length]);

    chart = d3.select(parent_id)
        .append('svg')
        .attr("class", 'chart')
        .attr('width', left_width + width)
        .attr('height', (bar_height + gap * 2) * data.length + 30)
        .append("g")

    chart.selectAll("rect")
        .data(data)
        .enter().append("rect")
        .attr("x", left_width)
        .attr("y", function(d,i) { return y(i) + gap; })
        .attr("width", function (d){return x(d.value);})
        .attr("height", bar_height)
        .attr("class", function (d){
            var class_name = "chart "+ d.code;
                if (special_one != undefined  && special_one == d.code){
                    class_name += " highlighted";
                }
                return class_name;
        })
    .on('click', click);

     chart.selectAll("text.score")
        .data(data)
        .enter().append("text")
        .attr("x", width)
        .attr("y", function(d, i){ return y(i) + y.rangeBand()/2; } )
        .attr("dx", -5)
        .attr("dy", ".30em")
        .attr("text-anchor", "end")
        .attr('class', 'score')
        .text(function(d){return "$"+d.pretty;});

    chart.selectAll("text.name")
        .data(data)
        .enter().append("text")
        .attr("x", left_width / 2)
        .attr("y", function(d, i){ return y(i) + y.rangeBand()/2;})
        .attr("dy", ".32em")
        .attr("dx", ".65em")
        .attr('class', 'name')
        .text(function(d){return d.name;})
        .call(wrap ,width - 60)
        .on('click', click);

    if(count_tooltip){
        console.log('tooltip on horizontal');
        $('svg text').tipsy({
        gravity: 's',
        html: true,
        title: count_tooltip

      });
    }
}

// adjust things when the window size changes
function resize_window() {
    if (document.getElementById('categories_sectors')){
        var div_id = '#categories_sectors'
        var data = window.horizontal_chart_data_selectable
        resize_horizontal_bar_chart(div_id, data)
    }
    if (document.getElementById("barchart_horizontal_donors_commitments")){
        var div_id = "#barchart_horizontal_donors_commitments"
        var data = window.horizontal_chart_data_1
        resize_horizontal_bar_chart(div_id, data)
    }
    if (document.getElementById("sector_commitments")){
        var div_id = "#sector_commitments"
        var data = window.horizontal_chart_data_2
        resize_horizontal_bar_chart(div_id, data)
    }
    if (document.getElementById("top_donors")){
        var div_id = "#top_donors"
        var data = window.horizontal_chart_data_1
        resize_horizontal_bar_chart(div_id, data)
    }
    if (document.getElementById("barchart_donors_commitments")){
        var div_id = "#barchart_donors_commitments"
        var data = window.bar_chart_data
        var legend_align = "end"
        resize_bar_chart(div_id, data, legend_align)
    }
    if (document.getElementById("donor_commitments")){
        var div_id = "#donor_commitments"
        var data = window.bar_chart_data
        var legend_align = "end"
        resize_bar_chart(div_id, data, legend_align)
    }
    if (document.getElementById("ministry_commitments")){
        var div_id = "#ministry_commitments"
        var data = window.bar_chart_data
        var legend_align = "start"
        resize_bar_chart(div_id, data, legend_align)
    }
}

function resize_horizontal_bar_chart(div_id, data){
    var width = parseInt(d3.select(div_id).style('width'));

    var x = d3.scale.linear()
        .domain([0, d3.max(data, function (d) {return d.value;})])
        .range([0, width]);

    var chart = d3.select(div_id)

    chart.select('svg').attr('width', width)

    chart.selectAll("rect")
        .attr("width", function (d){return x(d.value);})

    chart.selectAll("text.score")
        .attr("x", width)

    chart.selectAll("text.name")
        .data(data)
        .text(function(d){return d.name;})
        .call(wrap ,width-60)
}

function resize_bar_chart(div_id, data, legend_align){

    var width = parseInt(d3.select(div_id).style('width'));

    var x = d3.scale.ordinal()
        .rangeRoundBands([0, width-window.margin.left - window.margin.right], .1);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var chart = d3.select(div_id)

    chart.select("svg")
        .attr("width", width)

    x.domain(data.map(function (d) {
        return d.name;
    }));

    chart.selectAll(".bar")
        .data(data)
        .attr("x", function (d) {
            return x(d.name);
        })
        .attr("width", x.rangeBand());

    chart.select('.x.axis').call(xAxis)
        .selectAll("text")
        .style("text-anchor", legend_align)
        .attr("dx", "-.8em")
        .attr("dy", "-.6em");

}

function wrap(text, width) {
  text.each(function() {
    var text = d3.select(this),
        words = text.text().split(/\s+/).reverse(),
        word,
        line = [],
        lineNumber = 0,
        lineHeight = 1.1, // ems
        y = text.attr("y"),
        dy = parseFloat(text.attr("dy")),
        tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy + "em");

    while (word = words.pop()) {
      line.push(word);
      tspan.text(line.join(" "));

      if (tspan.node().getComputedTextLength() > width) {
            line.pop();
            tspan.text(line.join(" "));
      }

    }
  });
}

function draw_donut_into_div(parent_id, data, width, height, center_text) {
    if (data.length == 0){
        no_data_donut(parent_id, width, height);
        return;
    }
    var radius = Math.min(width, height) / 2;

    if(global_for_print){
        var offsetY = radius;
        var offsetX = -width/2 + global_legend_v_gap;
        height = height + (global_legend_box_height + global_legend_v_gap *2) * data.length;
    }


    var center_total = d3.sum(data, function(d){return d.value;});
    var color = d3.scale.ordinal()
        .range([ "#2996cc", "#5bb3de", "#93cde9", "#cce7f5", "#f6fbfd", "#ff8c00"]);

    var arc = d3.svg.arc()
        .outerRadius(radius - 10)
        .innerRadius(radius - 35);

    var pie = d3.layout.pie()
        .sort(null)
        .value(function (d) {
            return d.value;
        });

    var svg_donut = d3.select(parent_id).append("svg")
        .attr("width", '70%')
        .attr("height", '18%')
        .attr('viewBox','0 0 '+Math.min(width,height) +' '+Math.min(width,height) )
        .attr('preserveAspectRatio','xMinYMin')
        .append("g")
        .attr("transform", "translate(" + Math.min(width,height) / 2 + "," + Math.min(width,height) / 2 + ")");

    var g = svg_donut.selectAll(".arc")
        .data(pie(data))
        .enter().append("g")
        .attr("class", "arc");

    g.append("path")
        .attr("d", arc)
        .style("fill", function (d) {
            return color(d.data.code);
        })
        .transition()
            .ease("elastic")
            .duration(2000)
            .delay(200)     // this is 0.1s
            .attrTween("d", tweenPie);
    
    function tweenPie(b) {
      var i = d3.interpolate({startAngle: 1.1*Math.PI, endAngle: 1.1*Math.PI}, b);
      return function(t) { return arc(i(t)); };
    }
    

    if (center_text){

    svg_donut.append("text")
        .style("text-anchor", "middle")
        .attr("dy", "1.3em")
        .attr("class", "donut_center_title")
        .text(center_text);

    svg_donut.append("text")
        .style("text-anchor", "middle")
        .attr("dy", "0em")
        .attr("class", "donut_center_value")
        .text(center_total);
    }

    if(global_for_print){
        add_legend(svg_donut, offsetY, offsetX, data, color);
    }
    $('svg path').tipsy({
        gravity: 's',
        html: true,
        title: function() {
          var d = this.__data__;//, c = colors(d.i);
          if(d.data.hasOwnProperty('pretty')) {
            return d.data.name + "<br>"+ d.data.pretty;
          };
          return d.data.name + "<br>"+ d.value;// My color is <span style="color:' + c + '">' + c + '</span>';
        }

      });
}

function add_legend(element, top, left, data, color_fn){
    /* Legend: boxes */
    var bordercolor = "#444";
    var y = d3.scale.ordinal()
        .domain(data.map(function(d,i){return i;}))
        .rangeBands([0, (global_legend_box_height + 2 * global_legend_v_gap) * data.length]);

    element.selectAll("rect")
        .data(data)
        .enter().append("rect")
        .attr("x", left)
        .attr("y", function(d,i) { return top + y(i) + global_legend_v_gap; })
        .attr("width", global_legend_box_width)
        .attr("height", global_legend_box_height)
        .style("fill", function (d) {
            return color_fn(d.code);
        })
        .style("stroke", bordercolor)
        .style("stroke-width", 1);
    /* Legend: text */
    element.selectAll("text.name")
        .data(data)
        .enter().append("text")
        .attr("x", left + global_legend_box_width)
        .attr("y", function(d, i){ return top + y(i) + global_legend_box_height + global_legend_v_gap / 2;})
        .attr("dx", ".65em")
        .attr("text-anchor", "left")
        .attr('class', 'legend-text')
        .text(function(d){return d.name + " (" + d.value+")";});

}

function no_data_donut(element, width, height){

        var donut = d3.select(element).append("svg")
        .attr("width", '70%')
        .attr("height", '18%')
        .attr('viewBox','0 0 '+Math.min(width,height) +' '+Math.min(width,height) )
        .attr('preserveAspectRatio','xMinYMin')
        .append("g")
        .attr("transform", "translate(" + Math.min(width,height) / 2 + "," + Math.min(width,height) / 2 + ")");


    donut.append("text")
        .style("text-anchor", "middle")
        .attr("dy", "0em")
        .attr("class", "no_data")
        .text(global_no_data_text_donut_1);
    donut.append("text")
        .style("text-anchor", "middle")
        .attr("dy", "1.3em")
        .attr("class", "no_data")
        .text(global_no_data_text_donut_2);
}

function no_data_bar_chart(element, width, height){

    var chart = d3.select(element).append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")

    chart.append("text")
        .style("text-anchor", "middle")
        .attr("dy", "50%")
        .attr("dx", "50%")
        .attr("class", "no_data")
        .text(global_no_data_text);

}
