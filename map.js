
        $(function() {
	        $('#date').datepicker({onSelect: showDate});
        });
        
        function showDate(date){
          $('#map')
          
            var dateLayer = new OpenLayers.Layer.WMS($.format.date('' + date, 'MMdd'),
                "http://geoportal.waterqualitymap.eu/cgi-bin/mapserv?map=algae2010.map",
                {
                    layers: '' + $.format.date('' + date, 'MMdd'),
                    format: 'image/png',
                    transparent: true,
                },
                {
                    isBaseLayer: false,
                    buffer: 0,
                }
                );
            
            map.addLayer(dateLayer);
                    
         }
        
        $(function() {
          $('#map')
          
           map = new OpenLayers.Map ("map", {
				restrictedExtent: new OpenLayers.Bounds(-3, 51,
                                              6, 53.0),
				controls:[
					new OpenLayers.Control.Navigation(),
					new OpenLayers.Control.PanZoomBar(),
					new OpenLayers.Control.LayerSwitcher(),
					new OpenLayers.Control.Attribution()],
					allOverlays: true,
					
			} );
            var wms = new OpenLayers.Layer.WMS(
            "OpenLayers WMS",
            "http://labs.metacarta.com/wms/vmap0",
            {layers: 'basic'}
            );
            
            map.addLayer(wms);
            map.zoomToMaxExtent();
          
          });
