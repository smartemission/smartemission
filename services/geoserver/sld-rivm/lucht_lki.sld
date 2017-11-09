<?xml version="1.0" ?>
<sld:StyledLayerDescriptor version="1.0.0" xmlns="http://www.opengis.net/sld" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:sld="http://www.opengis.net/sld">
 <sld:UserLayer>
  <sld:LayerFeatureConstraints>
   <sld:FeatureTypeConstraint/>
  </sld:LayerFeatureConstraints>
  <sld:UserStyle>
   <sld:Title/>
   <sld:FeatureTypeStyle>
    <sld:Name/>
    <sld:Rule>
     <sld:RasterSymbolizer>
      <sld:Geometry>
       <ogc:PropertyName>grid</ogc:PropertyName>
      </sld:Geometry>
      <sld:Opacity>1</sld:Opacity>
      <sld:ColorMap type="intervals">
       <sld:ColorMapEntry color="#FFFFFF" label="Luchtkwaliteitsindex (LKI)" opacity="0.01" quantity="-1"/>
       <sld:ColorMapEntry color="#FFFFFF" label="kaart ververst elk uur" opacity="0.01" quantity="0"/>
       <sld:ColorMapEntry color="#0020C5" label="0.0-0.5     Goed" opacity="1.0" quantity="0.5"/>
       <sld:ColorMapEntry color="#002BF7" label="0.5-1.0     Goed" opacity="1.0" quantity="1"/>
       <sld:ColorMapEntry color="#006DF8" label="1.0-1.5     Goed" opacity="1.0" quantity="1.5"/>
       <sld:ColorMapEntry color="#009CF9" label="1.5-2.0     Goed" opacity="1.0" quantity="2"/>
       <sld:ColorMapEntry color="#2DCDFB" label="2.0-2.5     Goed" opacity="1.0" quantity="2.5"/>
       <sld:ColorMapEntry color="#C4ECFD" label="2.5-3.0     Goed" opacity="1.0" quantity="3"/>
       <sld:ColorMapEntry color="#FFFED0" label="3.0-3.6     Matig" opacity="1.0" quantity="3.6"/>
       <sld:ColorMapEntry color="#FFFDA4" label="3.6-4.2     Matig" opacity="1.0" quantity="4.2"/>
       <sld:ColorMapEntry color="#FFFD7B" label="4.2-4.8     Matig" opacity="1.0" quantity="4.8"/>
       <sld:ColorMapEntry color="#FFFC4D" label="4.8-5.4     Matig" opacity="1.0" quantity="5.4"/>
       <sld:ColorMapEntry color="#F4E645" label="5.4-6.0     Matig" opacity="1.0" quantity="6"/>
       <sld:ColorMapEntry color="#FFB255" label="6.0-6.7     Onvoldoende" opacity="1.0" quantity="6.7"/>
       <sld:ColorMapEntry color="#FF9845" label="6.7-7.4     Onvoldoende" opacity="1.0" quantity="7.4"/>
       <sld:ColorMapEntry color="#FE7626" label="7.4-8.0     Onvoldoende" opacity="1.0" quantity="8"/>
       <sld:ColorMapEntry color="#FF0A17" label="8.0-9.0     Slecht" opacity="1.0" quantity="9"/>
       <sld:ColorMapEntry color="#DC0610" label="9.0-10.0   Slecht" opacity="1.0" quantity="10"/>
       <sld:ColorMapEntry color="#A21794" label="10.0-11.0 Zeer slecht" opacity="1.0" quantity="999"/>
      </sld:ColorMap>
     </sld:RasterSymbolizer>
    </sld:Rule>
   </sld:FeatureTypeStyle>
  </sld:UserStyle>
 </sld:UserLayer>
</sld:StyledLayerDescriptor>