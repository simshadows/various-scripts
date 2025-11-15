<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format">

<xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes" />
 
<xsl:template match="node()|@*">
    <xsl:copy>
        <xsl:apply-templates select="node()|@*" />
    </xsl:copy>
</xsl:template>
 
<xsl:template match="Omegalul">
    <MonkaS bbb="{@aaa}"><xsl:value-of select=". + 1"/></MonkaS>
</xsl:template>
 
</xsl:stylesheet>