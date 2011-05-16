
        $(function() {
	        $('.date').datepick({onSelect: showDate});
        });
        
        function showDate(date){
          $('#map')
          
            var dateLayer = new OpenLayers.Layer.WMS($.format.date('' + date, 'MMdd'),
                "http://geoportal.waterqualitymap.eu/cgi-bin/mapserv?map=chl2011.map",
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
				controls:[
					new OpenLayers.Control.Navigation(),
					new OpenLayers.Control.PanZoomBar(),
					new OpenLayers.Control.LayerSwitcher(),
					new OpenLayers.Control.Attribution()],
					allOverlays: true

			} );
            var wms = new OpenLayers.Layer.WMS(
            "OpenLayers WMS",
            "http://labs.metacarta.com/wms/vmap0",
            {layers: 'basic'}
            );
            
            map.addLayer(wms);
            map.zoomToMaxExtent();
          
          });