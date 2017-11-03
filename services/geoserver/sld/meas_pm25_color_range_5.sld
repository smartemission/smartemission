<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0"
                       xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd"
                       xmlns="http://www.opengis.net/sld"
                       xmlns:ogc="http://www.opengis.net/ogc"
                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

    <!-- a Named Layer is the basic building block of an SLD document -->
    <NamedLayer>
        <Name>Measurements PM2.5</Name>
        <Name>Measurements PM2.5 ug/m3</Name>
        <UserStyle>
            <!-- Styles can have names, titles and abstracts -->
            <Title>Smart Emission measurements PM2.5</Title>
            <Abstract>Smart Emission measurements_pm2.5 style</Abstract>
            <IsDefault>1</IsDefault>
            <!-- FeatureTypeStyles describe how to render different features -->

            <!-- A FeatureTypeStyle for rendering points -->
            <FeatureTypeStyle>
                <Rule>
                    <Name>0 - 20 ug/m3</Name>
                    <Title>  0 - 20 ug/m3 Goed</Title>
                    <ogc:Filter>
                        <ogc:PropertyIsLessThan>
                            <ogc:PropertyName>value</ogc:PropertyName>
                            <ogc:Literal>19.5</ogc:Literal>
                        </ogc:PropertyIsLessThan>
                    </ogc:Filter>
                    <PointSymbolizer>
                        <Graphic>
                            <Mark>
                                <!-- Blue -->
                                <WellKnownName>circle</WellKnownName>
                                <Fill>
                                    <CssParameter name="fill">#3399CC</CssParameter>
                                    <CssParameter name="fill-opacity">1.0</CssParameter>
                                </Fill>
                                <Stroke>
                                     <CssParameter name="stroke">#EEEEEE</CssParameter>
                                     <CssParameter name="stroke-width">1</CssParameter>
                                 </Stroke>
                            </Mark>
                            <Size>20</Size>
                        </Graphic>
                    </PointSymbolizer>
                </Rule>
                <Rule>
                    <Name>20 - 50 ug/m3</Name>
                    <Title>  20 - 50 ug/m3 Matig</Title>
                    <ogc:Filter>
                        <ogc:And>
                            <ogc:PropertyIsGreaterThan>
                                <ogc:PropertyName>value</ogc:PropertyName>
                                <ogc:Literal>19.5</ogc:Literal>
                            </ogc:PropertyIsGreaterThan>
                            <ogc:PropertyIsLessThan>
                                <ogc:PropertyName>value</ogc:PropertyName>
                                <ogc:Literal>59.5</ogc:Literal>
                            </ogc:PropertyIsLessThan>
                        </ogc:And>
                    </ogc:Filter>
                    <PointSymbolizer>
                        <Graphic>
                            <Mark>
                                <WellKnownName>circle</WellKnownName>
                                <Fill>
                                    <CssParameter name="fill">#FFFF00</CssParameter>
                                </Fill>
                                <Stroke>
                                     <CssParameter name="stroke">#EEEEEE</CssParameter>
                                     <CssParameter name="stroke-width">1</CssParameter>
                                 </Stroke>
                            </Mark>
                            <Size>20</Size>
                        </Graphic>
                    </PointSymbolizer>
                </Rule>
                <Rule>
                    <Name>50 - 90 ug/m3</Name>
                    <Title>  50 - 90 ug/m3 Onvoldoende</Title>
                    <ogc:Filter>
                        <ogc:And>
                            <ogc:PropertyIsGreaterThan>
                                <ogc:PropertyName>value</ogc:PropertyName>
                                <ogc:Literal>49.5</ogc:Literal>
                            </ogc:PropertyIsGreaterThan>
                            <ogc:PropertyIsLessThan>
                                <ogc:PropertyName>value</ogc:PropertyName>
                                <ogc:Literal>89.5</ogc:Literal>
                            </ogc:PropertyIsLessThan>
                        </ogc:And>
                    </ogc:Filter>
                    <PointSymbolizer>
                        <Graphic>
                            <Mark>
                                <WellKnownName>circle</WellKnownName>
                                <Fill>
                                    <CssParameter name="fill">#FF9900</CssParameter>
                                </Fill>
                                <Stroke>
                                     <CssParameter name="stroke">#EEEEEE</CssParameter>
                                     <CssParameter name="stroke-width">1</CssParameter>
                                 </Stroke>
                            </Mark>
                            <Size>20</Size>
                        </Graphic>
                    </PointSymbolizer>
                </Rule>
                <Rule>
                    <Name>90 - 140 ug/m3</Name>
                    <Title>  90 - 140 ug/m3 Slecht</Title>
                    <ogc:Filter>
                        <ogc:And>
                            <ogc:PropertyIsGreaterThan>
                                <ogc:PropertyName>value</ogc:PropertyName>
                                <ogc:Literal>89.5</ogc:Literal>
                            </ogc:PropertyIsGreaterThan>
                            <ogc:PropertyIsLessThan>
                                <ogc:PropertyName>value</ogc:PropertyName>
                                <ogc:Literal>139.5</ogc:Literal>
                            </ogc:PropertyIsLessThan>
                        </ogc:And>
                    </ogc:Filter>
                    <PointSymbolizer>
                        <Graphic>
                            <Mark>
                                <WellKnownName>circle</WellKnownName>
                                <Fill>
                                    <CssParameter name="fill">#FF0000</CssParameter>
                                </Fill>
                                <Stroke>
                                     <CssParameter name="stroke">#EEEEEE</CssParameter>
                                     <CssParameter name="stroke-width">1</CssParameter>
                                 </Stroke>
                            </Mark>
                            <Size>20</Size>
                        </Graphic>
                    </PointSymbolizer>
                </Rule>
                <Rule>
                    <Name>140 - MAX ug/m3</Name>
                    <Title>  &gt; 140 ug/m3 Zeer Slecht</Title>
                    <ogc:Filter>
                        <ogc:PropertyIsGreaterThan>
                            <ogc:PropertyName>value</ogc:PropertyName>
                            <ogc:Literal>139.5</ogc:Literal>
                        </ogc:PropertyIsGreaterThan>
                    </ogc:Filter>
                    <PointSymbolizer>
                        <Graphic>
                            <Mark>
                                <WellKnownName>circle</WellKnownName>
                                <Fill>
                                    <CssParameter name="fill">#660099</CssParameter>
                                </Fill>
                                <Stroke>
                                     <CssParameter name="stroke">#EEEEEE</CssParameter>
                                     <CssParameter name="stroke-width">1</CssParameter>
                                 </Stroke>
                            </Mark>
                            <Size>20</Size>
                        </Graphic>
                    </PointSymbolizer>
                </Rule>
                <Rule>
                    <!--<Name>Sample Value</Name>-->
                    <!--<Title>  Sample Value ug/m3</Title>-->

                    <!--<TextSymbolizer>-->
                        <!--<Label>-->
                            <!--<ogc:Function name="numberFormat">-->
                                <!--<ogc:Literal>##</ogc:Literal>-->
                                <!--<ogc:PropertyName>value</ogc:PropertyName>-->
                            <!--</ogc:Function>-->
                        <!--</Label>-->

                        <!--<Font>-->
                            <!--<CssParameter name="font-family">-->
                                <!--<ogc:Literal>SansSerif</ogc:Literal>-->
                            <!--</CssParameter>-->

                            <!--<CssParameter name="font-size">-->
                                <!--<ogc:Literal>10</ogc:Literal>-->
                            <!--</CssParameter>-->
                            <!--<CssParameter name="font-weight">-->
                                <!--<ogc:Literal>bold</ogc:Literal>-->
                            <!--</CssParameter>-->
                        <!--</Font>-->
                        <!--<LabelPlacement>-->
                            <!--<PointPlacement>-->
                                <!--<AnchorPoint>-->
                                    <!--<AnchorPointX>0.5</AnchorPointX>-->
                                    <!--<AnchorPointY>0.5</AnchorPointY>-->
                                <!--</AnchorPoint>-->
                            <!--</PointPlacement>-->
                        <!--</LabelPlacement>-->

                        <!--<Fill>-->
                            <!--<CssParameter name="fill">#FFCCFF</CssParameter>-->
                        <!--</Fill>-->

                    <!--</TextSymbolizer>-->
                </Rule>
            </FeatureTypeStyle>
        </UserStyle>
    </NamedLayer>
</StyledLayerDescriptor>
