<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0"
    xpath-default-namespace="http://www.abbyy.com/FineReader_xml/FineReader8-schema-v2.xml" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    > <xsl:strip-space elements="*"/>
    <xsl:output indent="no" method="text" encoding="UTF-8"/>
    <xsl:template match="line">
        
<!--        Zeile auswählen   -->
        <xsl:variable name="line">
            <xsl:value-of select="formatting/charParams"/>
        </xsl:variable>
<!--    Zeile formatieren  -->
        <xsl:variable name="line1">
            <xsl:value-of select="replace($line,' {2}','#')"/>
        </xsl:variable>
        <xsl:variable name="line2">
            <xsl:value-of select="replace($line1,' ','')"/>
        </xsl:variable>
        <xsl:variable name="line3">
            <xsl:value-of select="replace($line2,'#',' ')"/>
        </xsl:variable>
     <xsl:value-of select="$line3"/><xsl:text>&#10;</xsl:text>
    
    </xsl:template>
</xsl:stylesheet>