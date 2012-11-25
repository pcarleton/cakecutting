google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(drawVisualization);
function drawVisualization() {
  // Create and populate the data table.
  var prefs1 = getPrefs();
  var prefs2 = { points: [[0, 1], [1, 1]], }; 

  prefs2.scaleFactor = 1.0/getAreaUnderneath(prefs2.points);
  
  var maxVal = 1;
  var data = new google.visualization.DataTable();

  data.addColumn('number', 'x');
  data.addColumn('number', 'Prefs1');
  data.addColumn('number', 'Prefs2');


  var pref1Index = 0;
  var pref2Index = 0;

  while (pref1Index < prefs1.points.length && pref2Index < prefs2.points.length) {
    var nextp1 = prefs1.points[pref1Index];
    var nextp2 = prefs2.points[pref2Index];

    console.log(nextp1);
    console.log(nextp2);

    if (nextp1 && nextp1[0] == nextp2[0]) {
      data.addRow([nextp1[0],
                  nextp1[1] * prefs1.scaleFactor,
                  nextp2[1] * prefs2.scaleFactor,]);
      pref1Index++;
      pref2Index++;
    } else if (nextp1 && nextp1[0] < nextp2[0]) {
      data.addRow([prefs1.points[pref1Index][0],
                  prefs1.points[pref1Index][1] *prefs1.scaleFactor, null]);
      pref1Index++;
    } else {
      data.addRow([prefs2.points[pref2Index][0],
                  prefs2.points[pref2Index][1] * prefs.scaleFactor, null]);
      pref2Index++;
    }
  }

  console.log(data);




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


function getPrefs() {
  var lines = $("#prefs1").val().replace(/\r\n/g, "\n").split("\n");

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
});
