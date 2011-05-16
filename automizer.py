#!/usr/bin/python
import os, sys, datetime, subprocess
from fileinput import input

mapfile = '/home/fritz/WebDev/algae2011.map'
txt = '/home/fritz/WebDev/layers.txt'
js = '/home/fritz/WebDev/datepick/map.js'

def get_date_mapfile(mapfile, txt):
    print "getting mapfile, writing dates to txtfile"
    readdates = """grep -E "NAME" """ + mapfile + """ | sed -e 's/[^0-9]//g' -e '/^$/ d' > """ + txt
    subprocess.call(readdates, shell=True)

rtxt = open(txt)
wjs = open(js, "w")
maps = []

def read_write_dates():
    print "reading text file saving dates as datetime objects"
    read_it = rtxt.readlines()
    del read_it[0:1]
    for lines in read_it:
        line = lines.strip()
        year = int(line[0:4])
        month = int(line[4:6])
        day = int(line[6:8])
        datum = datetime.date(year, month, day)
        maps.append(datum)

def write_maps_to_js():
    print "Array with dates that should be enabled in DatePicker"
    wjs.write("""/**
     *

    /** Fritz van Deventer == Water Insight
     *  Gratefully used and edited OpenLayers examples and Datepicker.
     *  
     *  
     */
     """)
    for i in range(len(maps)):
        wjs.write(''' "'''+  map_.strftime('%m%d') +'''", ''')


    wjs.write("""
    var mapPanel, tree;
    Ext.onReady(function() {
        // create a map panel with some layers that we will show in our layer tree
        // below.
        mapPanel = new GeoExt.MapPanel({
            border: true,
            region: "center",
            // we do not want all overlays, to try the OverlayLayerContainer
            map: new OpenLayers.Map({allOverlays: true}),
            center: [1.0, 52.0],
            zoom: 6,
            layers: [
                new OpenLayers.Layer.WMS("OpenStreetMap",
                    "http://labs.metacarta.com/wms/vmap0", {
                        layers: "basic"
                    }, {
                        buffer: 0,
                        visibility: true
                    }
                ),
    """
            )

    for i in range(len(maps)):
        if maps[i].month != maps[i-1].month:
            month = maps[i].month
            wjs.write('''
                new OpenLayers.Layer.WMS("'''+ maps[i].strftime('%h%Y') +'''",
            "http://geoportal.waterqualitymap.eu/cgi-bin/mapserv?map=chl2011.map",
            {
                layers: '''+ maps[i].strftime('%h') +'''Layers,
                transparent: true,
                format: "image/png"
                        }, 
                {
                    isBaseLayer: false,
                    buffer: 0,
                    // exclude this layer from layer container nodes
                    displayInLayerSwitcher: true,
                    visibility: false
                }
             ),
             ''')

    wjs.write("""
            ]
        });

        // create our own layer node UI class, using the TreeNodeUIEventMixin
        var LayerNodeUI = Ext.extend(GeoExt.tree.LayerNodeUI, new GeoExt.tree.TreeNodeUIEventMixin());
            
        // using OpenLayers.Format.JSON to create a nice formatted string of the
        // configuration for editing it in the UI
        var treeConfig = new OpenLayers.Format.JSON().write([{
            nodeType: "gx_baselayercontainer"
        },
        """)
    for i in range(len(maps)):
        if maps[i].month != maps[i-1].month:
            month = maps[i].month
            wjs.write('''{
            nodeType: "gx_layer",
            layer: "'''+ maps[i].strftime('%h%Y') +'''",
            isLeaf: false,
            // create subnodes for the layers in the LAYERS param. If we assign
            // a loader to a LayerNode and do not provide a loader class, a
            // LayerParamLoader will be assumed.
            loader: {
                param: "LAYERS"
            },
            baseAttrs: {
                checkedGroup: "chl"
            }
            }, 
            ''')

    wjs.write("""
        ], true);      
        // create the tree with the configuration from above
        tree = new Ext.tree.TreePanel({
            border: true,
            region: "west",
            title: "Layers",
            width: 200,
            split: true,
            collapsible: true,
            collapseMode: "mini",
            autoScroll: true,
            plugins: [
                new GeoExt.plugins.TreeNodeRadioButton({
                    listeners: {
                        "radiochange": function(node) {
                            alert(node.text + " is now the active layer.");
                        }
                    }
                })
            ],
            loader: new Ext.tree.TreeLoader({
                // applyLoader has to be set to false to not interfer with loaders
                // of nodes further down the tree hierarchy
                applyLoader: false,
                uiProviders: {
                    "layernodeui": LayerNodeUI
                }
            }),
            root: {
                nodeType: "async",
                // the children property of an Ext.tree.AsyncTreeNode is used to
                // provide an initial set of layer nodes. We use the treeConfig
                // from above, that we created with OpenLayers.Format.JSON.write.
                children: Ext.decode(treeConfig)
            },
            rootVisible: false,
            lines: false,
        });

        // dialog for editing the tree configuration
        var treeConfigWin = new Ext.Window({
            layout: "fit",
            hideBorders: true,
            closeAction: "hide",
            width: 300,
            height: 400,
            title: "Tree Configuration",
            items: [{
                xtype: "form",
                layout: "fit",
                items: [{
                    id: "treeconfig",
                    xtype: "textarea"
                }],
                buttons: [{
                    text: "Save",
                    handler: function() {
                        var value = Ext.getCmp("treeconfig").getValue()
                        try {
                            var root = tree.getRootNode();
                            root.attributes.children = Ext.decode(value);
                            tree.getLoader().load(root);
                        } catch(e) {
                            alert("Invalid JSON");
                            return;
                        }
                        treeConfig = value;
                        treeConfigWin.hide();
                    }
                }, {
                    text: "Cancel",
                    handler: function() {
                        treeConfigWin.hide();
                    }
                }]
            }]
        });
        
        new Ext.Viewport({
            layout: "fit",
            hideBorders: true,
            items: {
                layout: "border",
                deferredRender: false,
                items: [mapPanel, tree, {
                    contentEl: "desc",
                    region: "east",
                    bodyStyle: {"padding": "5px"},
                    collapsible: true,
                    collapseMode: "mini",
                    split: true,
                    width: 200,
                    title: "Description"
                }]
            }
        });
    });
    """)

    wjs.close()

get_date_mapfile(mapfile, txt)
read_write_dates()
write_maps_to_js()
