google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(drawVisualization);
function drawVisualization() {
  // Create and populate the data table.
  var prefs1 = getPrefs(1);
  var prefs2 = getPrefs(2);
  var prefs3 = getPrefs(3);

  var prefs = [prefs1, prefs2, prefs3];
  
  var maxVal = 1;
  var data = new google.visualization.DataTable();

  data.addColumn('number', 'x');
  data.addColumn('number', 'Prefs1');
  data.addColumn('number', 'Prefs2');
  data.addColumn('number', 'Prefs3');


  var pref1Index = 0;
  var pref2Index = 0;
  var pref3Index = 0;

  while (pref1Index < prefs1.points.length && pref2Index < prefs2.points.length && pref3Index < prefs3.points.length) {
    var nextp1 = prefs1.points[pref1Index] || [99, 0];
    var nextp2 = prefs2.points[pref2Index] || [99, 0];
    var nextp3 = prefs3.points[pref3Index] || [99, 0];

    var nextX = Math.min(nextp1[0], nextp2[0], nextp3[0]);

    var p1val, p2val, p3val;

    p1val = (nextp1[0] == nextX) ? nextp1[1]*prefs1.scaleFactor : null;
    p2val = (nextp2[0] == nextX) ? nextp2[1]*prefs2.scaleFactor : null;
    p3val = (nextp3[0] == nextX) ? nextp3[1]*prefs3.scaleFactor : null;

    if (p1val != null) { pref1Index++; }
    if (p2val != null) { pref2Index++; }
    if (p3val != null) { pref3Index++; }

    data.addRow([nextX, p1val, p2val, p3val]);
  }



  // Create and draw the visualization.
  new google.visualization.LineChart(document.getElementById('visualization')).
      draw(data, {curveType: "line",
                  width: 500, height: 400,
                  interpolateNulls: true}
          );
}


function getAreaUnderneath(listOfPoints) {
  var oldx = 0.0;
  var oldy = 0.0;

  var accumulator = 0.0;

  for (var i = 0; i < listOfPoints.length; i++) {
    console.log("Point " + String(i));
    var curPoint = listOfPoints[i];
    var x = curPoint[0];
    var y = curPoint[1];
    var curArea = 0;

    if (x == 0) {
      console.log("x " + String(x) + "y: " + String(y));
      oldy = y;
    } else {
      console.log("Oldx " + String(oldx) + "Oldy: " + String(oldy));
      console.log("x " + String(x) + "y: " + String(y));
      curArea = calculateArea(oldx, oldy, x, y);
      accumulator += curArea;
      oldx = x;
      oldy = y;
    }
  }
  if (oldx < 1.0) {
    accumulator += calculateArea(oldx, oldy, 1, 0);
  }
  return accumulator;
}


function calculateArea(x1, y1, x2, y2) {

  var m = (y2-y1)/(x2-x1)*1.0;
  var b = 1.0*y1 - m*x1;


  console.log("m: " + String(m) + " b: " + String(b));

  var leftSide = m*x1*x1/2.0 + b*x1;
  var rightSide = m*x2*x2/2.0 + b*x2;

  return rightSide - leftSide;
}


function getPrefs(i) {
  var lines = $("#prefs" + String(i)).val().replace(/\r\n/g, "\n").split("\n");

  var curPoint;
  var prefs = {};
  prefs.points = [];
  for (var i = 0; i < lines.length; i++) {
    var line = lines[i];
    var values = line.split(" ");
    curPoint = [parseFloat(values[0]), parseFloat(values[1])];

    prefs.points.push(curPoint);
  }


  prefs.scaleFactor = 1.0/getAreaUnderneath(prefs.points);
  return prefs;
}


$(function() {
  $("#graphIt").click( function() {
    drawVisualization();
  });

  $("#submit").click( function() {
    $.get("runstrom", function( data ) {
      $("#holder").html(data);
    });

  });
});
