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
       <sld:ColorMapEntry color="#FFFFFF" label="Stikstofdioxide (µg/m³)" opacity="0.01" quantity="-1"/>
       <sld:ColorMapEntry color="#FFFFFF" label="kaart ververst elk uur" opacity="0.01" quantity="0"/>
       <sld:ColorMapEntry color="#0020C5" label="0-5          Goed" opacity="1.0" quantity="5"/>
       <sld:ColorMapEntry color="#002BF7" label="5-10        Goed" opacity="1.0" quantity="10"/>
       <sld:ColorMapEntry color="#006DF8" label="10-15      Goed" opacity="1.0" quantity="15"/>
       <sld:ColorMapEntry color="#009CF9" label="15-20      Goed" opacity="1.0" quantity="20"/>
       <sld:ColorMapEntry color="#2DCDFB" label="20-25      Goed" opacity="1.0" quantity="25"/>
       <sld:ColorMapEntry color="#C4ECFD" label="25-30      Goed" opacity="1.0" quantity="30"/>
       <sld:ColorMapEntry color="#FFFED0" label="30-39      Matig" opacity="1.0" quantity="39"/>
       <sld:ColorMapEntry color="#FFFDA4" label="39-48      Matig" opacity="1.0" quantity="48"/>
       <sld:ColorMapEntry color="#FFFD7B" label="48-57      Matig" opacity="1.0" quantity="57"/>
       <sld:ColorMapEntry color="#FFFC4D" label="57-66      Matig" opacity="1.0" quantity="66"/>
       <sld:ColorMapEntry color="#F4E645" label="66-75      Matig" opacity="1.0" quantity="75"/>
       <sld:ColorMapEntry color="#FFB255" label="75-93      Onvoldoende" opacity="1.0" quantity="92.5"/>
       <sld:ColorMapEntry color="#FF9845" label="93-110    Onvoldoende" opacity="1.0" quantity="110"/>
       <sld:ColorMapEntry color="#FE7626" label="110-125  Onvoldoende" opacity="1.0" quantity="125"/>
       <sld:ColorMapEntry color="#FF0A17" label="125-150  Slecht" opacity="1.0" quantity="150"/>
       <sld:ColorMapEntry color="#DC0610" label="150-200  Slecht" opacity="1.0" quantity="200"/>
       <sld:ColorMapEntry color="#A21794" label="> 200      Zeer slecht" opacity="1.0" quantity="999"/>
      </sld:ColorMap>
     </sld:RasterSymbolizer>
    </sld:Rule>
   </sld:FeatureTypeStyle>
  </sld:UserStyle>
 </sld:UserLayer>
</sld:StyledLayerDescriptor>