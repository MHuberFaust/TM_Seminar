<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:mets="http://www.loc.gov/METS/" xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:vls="http://semantics.de/vls"
    xmlns="http://www.loc.gov/mods/v3" 
    xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-4.xsd"
    >

    
    <xsl:template match="mets:dmdSec">
        <xsl:variable name="filename">
           <xsl:value-of select="mets:mdWrap/mets:xmlData/*[namespace-uri()='http://www.loc.gov/mods/v3' and local-name()='mods'][1]/*[namespace-uri()='http://www.loc.gov/mods/v3' and local-name()='titleInfo'][1]/*[namespace-uri()='http://www.loc.gov/mods/v3' and local-name()='title'][1]"/>
         </xsl:variable>
        <xsl:variable name="ordner">
           <xsl:value-of select="mets:mdWrap/mets:xmlData/*[namespace-uri()='http://www.loc.gov/mods/v3' and local-name()='mods'][1]/*[namespace-uri()='http://www.loc.gov/mods/v3' and local-name()='originInfo'][1]/*[namespace-uri()='http://www.loc.gov/mods/v3' and local-name()='dateIssued'][1]"/>
        </xsl:variable>

        <xsl:variable name="ORDBEGINN">
            <xsl:value-of select="mets:mdWrap/mets:xmlData/*[namespace-uri()='http://www.loc.gov/mods/v3' and local-name()='mods'][1]/*[namespace-uri()='http://www.loc.gov/mods/v3' and local-name()='relatedItem'][1]/*[namespace-uri()='http://www.loc.gov/mods/v3' and local-name()='part'][1]/*[namespace-uri()='http://www.loc.gov/mods/v3' and local-name()='extent'][1]/*[namespace-uri()='http://www.loc.gov/mods/v3' and local-name()='start']"/>
        </xsl:variable>
        <xsl:variable name="ORDEND">
            <xsl:value-of select="mets:mdWrap/mets:xmlData/*[namespace-uri()='http://www.loc.gov/mods/v3' and local-name()='mods'][1]/*[namespace-uri()='http://www.loc.gov/mods/v3' and local-name()='relatedItem'][1]/*[namespace-uri()='http://www.loc.gov/mods/v3' and local-name()='part'][1]/*[namespace-uri()='http://www.loc.gov/mods/v3' and local-name()='extent'][1]/*[namespace-uri()='http://www.loc.gov/mods/v3' and local-name()='end']"/>
        </xsl:variable>
        <xsl:variable name="filenamepro">
            <xsl:value-of select="replace($filename,'[?:]',' ')"/>    
        </xsl:variable>
        
        <xsl:variable name="ID"><xsl:value-of select="@ID"/></xsl:variable>
        <xsl:variable name="ID2"><xsl:value-of select="substring($ID,3,6)"/></xsl:variable>
        <xsl:variable name="IDlog"><xsl:value-of select="concat('log',$ID2)"/></xsl:variable>
       
        
        
        
        
        
        
        <!-- Hier der Pfad Ordner der erstellt werden soll           -->   
        <xsl:result-document method="xml" href="ordered/{$ordner}/{$filenamepro}{$ORDBEGINN}.xml">
        
            <xsl:for-each select="/mets:mets/mets:structLink/mets:smLink[@xlink:from=$IDlog]/@xlink:to">
                
             
                <xsl:variable name="processed">
                    <xsl:value-of select="replace(.,'phys','')"/>    
                </xsl:variable>

            <xsl:variable name="fin2">
<!-- Hier der Pfad zum Ordner in dem die einzelnen alten Files liegen             -->
                <xsl:value-of select="concat('/home/leonard/Desktop/TopicModelling/Testdatenset/processed/',$processed,'.xml')"/>
            </xsl:variable>
         
             <doc><xsl:copy-of select="document($fin2)"/></doc>
            
        
            </xsl:for-each> 
        </xsl:result-document>
            
            
       
        
    </xsl:template>

</xsl:stylesheet>