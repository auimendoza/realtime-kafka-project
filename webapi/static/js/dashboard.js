     $(document).ready(function(){
       var gallons = {}; 
       namespace = '';

       var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

       socket.on('update', function(msg) {    
         if (msg.type == 'status') {
           $('#updatestatus').text(msg.status);
         } else if (msg.type == 'data') {
           $('#updatestatus').text(msg.data);
         }
       });

       socket.on('connect', function(){    
         socket.emit('connected');
       });

       var tcolor = {};
           tcolor['WC'] = '#ff99cc';
           tcolor['TX'] = '#ffcc99';
           tcolor['NYC'] = 'red';
           tcolor['NE'] = '#99ccff';
           tcolor['GL'] = '#ff9999';
           tcolor['SE'] = '#cc99ff';

        var map = new Datamap({
          scope: 'usa',
          element: document.getElementById('mapcontainer'),
          geographyConfig: {
              highlightOnHover: false,
              popupTemplate: function(geo, data) {
                  if (!data) { return ; }
                  return ['<div class="hoverinfo">',
                      '<strong>', data.territory, '</strong>',
                      '<br>Gallons: <strong>', data.gallons, '</strong>',
                      '</div>'].join('');
              }
          },
          projection: 'mercator',
          height: 500,
          fills: {
            defaultFill: '#e0e0e0',
            "WC": tcolor['WC'],
            "TX": tcolor['TX'],
            "NYC": tcolor['NYC'],
            "NE": tcolor['NE'],
            "GL": tcolor['GL'],
            "SE": tcolor['SE']
          },
          data: {
            AK: {fillKey: 'WC', territory:'West Coast', gallons: '-'},
            CA: {fillKey: 'WC', territory:'West Coast', gallons: '-'},
            OR: {fillKey: 'WC', territory:'West Coast', gallons: '-'},
            WA: {fillKey: 'WC', territory:'West Coast', gallons: '-'},
            TX: {fillKey: 'TX', territory:'Texas', gallons: '-'},
            CT: {fillKey: 'NE', territory:'North East', gallons: '-'},
            DE: {fillKey: 'NE', territory:'North East', gallons: '-'},
            MA: {fillKey: 'NE', territory:'North East', gallons: '-'},
            MD: {fillKey: 'NE', territory:'North East', gallons: '-'},
            ME: {fillKey: 'NE', territory:'North East', gallons: '-'},
            NH: {fillKey: 'NE', territory:'North East', gallons: '-'},
            NJ: {fillKey: 'NE', territory:'North East', gallons: '-'},
            NY: {fillKey: 'NE', territory:'North East', gallons: '-'},
            PA: {fillKey: 'NE', territory:'North East', gallons: '-'},
            RI: {fillKey: 'NE', territory:'North East', gallons: '-'},
            VA: {fillKey: 'NE', territory:'North East', gallons: '-'},
            VT: {fillKey: 'NE', territory:'North East', gallons: '-'},
            WV: {fillKey: 'NE', territory:'North East', gallons: '-'},
            IL: {fillKey: 'GL', territory:'Great Lakes', gallons: '-'},
            IN: {fillKey: 'GL', territory:'Great Lakes', gallons: '-'},
            MI: {fillKey: 'GL', territory:'Great Lakes', gallons: '-'},
            MN: {fillKey: 'GL', territory:'Great Lakes', gallons: '-'},
            OH: {fillKey: 'GL', territory:'Great Lakes', gallons: '-'},
            WI: {fillKey: 'GL', territory:'Great Lakes', gallons: '-'},
            AL: {fillKey: 'SE', territory:'South East', gallons: '-'},
            AR: {fillKey: 'SE', territory:'South East', gallons: '-'},
            FL: {fillKey: 'SE', territory:'South East', gallons: '-'},
            GA: {fillKey: 'SE', territory:'South East', gallons: '-'},
            KY: {fillKey: 'SE', territory:'South East', gallons: '-'},
            LA: {fillKey: 'SE', territory:'South East', gallons: '-'},
            MS: {fillKey: 'SE', territory:'South East', gallons: '-'},
            NC: {fillKey: 'SE', territory:'South East', gallons: '-'},
            SC: {fillKey: 'SE', territory:'South East', gallons: '-'},
            TN: {fillKey: 'SE', territory:'South East', gallons: '-'},
          }
        });
       map.bubbles([{
          name: 'New York Metro',
          gallons: '-',
          radius: 10,
          fillKey: 'NYC',
          latitude: 40.7773,
          longitude: -73.8727
        }]);
     });
