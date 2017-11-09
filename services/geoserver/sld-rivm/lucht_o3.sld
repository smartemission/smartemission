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
       <sld:ColorMapEntry color="#FFFFFF" label="Ozon (µg/m³)" opacity="0.01" quantity="-1"/>
       <sld:ColorMapEntry color="#FFFFFF" label="kaart ververst elk uur" opacity="0.01" quantity="0"/>
       <sld:ColorMapEntry color="#0020C5" label="0-8          Goed" opacity="1.0" quantity="7.5"/>
       <sld:ColorMapEntry color="#002BF7" label="8-15        Goed" opacity="1.0" quantity="15"/>
       <sld:ColorMapEntry color="#006DF8" label="15-23      Goed" opacity="1.0" quantity="22.5"/>
       <sld:ColorMapEntry color="#009CF9" label="23-30      Goed" opacity="1.0" quantity="30"/>
       <sld:ColorMapEntry color="#2DCDFB" label="30-35      Goed" opacity="1.0" quantity="35"/>
       <sld:ColorMapEntry color="#C4ECFD" label="35-40      Goed" opacity="1.0" quantity="40"/>
       <sld:ColorMapEntry color="#FFFED0" label="40-52      Matig" opacity="1.0" quantity="52"/>
       <sld:ColorMapEntry color="#FFFDA4" label="52-64      Matig" opacity="1.0" quantity="64"/>
       <sld:ColorMapEntry color="#FFFD7B" label="64-76      Matig" opacity="1.0" quantity="76"/>
       <sld:ColorMapEntry color="#FFFC4D" label="76-88      Matig" opacity="1.0" quantity="88"/>
       <sld:ColorMapEntry color="#F4E645" label="88-100    Matig" opacity="1.0" quantity="100"/>
       <sld:ColorMapEntry color="#FFB255" label="100-128  Onvoldoende" opacity="1.0" quantity="128"/>
       <sld:ColorMapEntry color="#FF9845" label="128-156  Onvoldoende" opacity="1.0" quantity="156"/>
       <sld:ColorMapEntry color="#FE7626" label="156-180  Onvoldoende" opacity="1.0" quantity="180"/>
       <sld:ColorMapEntry color="#FF0A17" label="180-200  Slecht" opacity="1.0" quantity="200"/>
       <sld:ColorMapEntry color="#DC0610" label="200-240  Slecht" opacity="1.0" quantity="240"/>
       <sld:ColorMapEntry color="#A21794" label="> 240      Zeer slecht" opacity="1.0" quantity="999"/>
      </sld:ColorMap>
     </sld:RasterSymbolizer>
    </sld:Rule>
   </sld:FeatureTypeStyle>
  </sld:UserStyle>
 </sld:UserLayer>
</sld:StyledLayerDescriptor>