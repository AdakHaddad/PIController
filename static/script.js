document.addEventListener("DOMContentLoaded", function () {
  fetch("/simulate")
    .then((response) => response.json())
    .then((data) => {
      var trace1 = {
        x: data.t,
        y: data.V1,
        mode: "lines",
        name: "V1 (V)",
      };

      var trace2 = {
        x: data.t,
        y: data.V2,
        mode: "lines",
        name: "V2 (V)",
      };

      var trace3 = {
        x: data.t,
        y: data.Idc12,
        mode: "lines",
        name: "Idc12 (A)",
      };

      var layout = {
        title: "Simulasi Tegangan dan Arus dalam Sistem DC",
        xaxis: { title: "Waktu (s)" },
        yaxis: { title: "Tegangan (V) / Arus (A)" },
      };

      var data = [trace1, trace2, trace3];

      Plotly.newPlot("plot", data, layout);
    });
});
