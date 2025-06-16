<?xml version="1.0" encoding="iso-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
	<html>
		<head>
			<link rel="stylesheet" type="text/css" href=".\Resources\Log.css" />
			<style type="text/css"></style>
		</head>
		<h1>
			<xsl:value-of select="@Date" />
		</h1>
		<body style="font-family:Verdana; font-size:18px">
			<xsl:apply-templates />
		</body>
	</html>
</xsl:template>

<xsl:template match="Logging">
	<h1 align="center">Logger:
	  <xsl:value-of select="@Date" />
	</h1>
	<table class="Logtable" align="center">
		<tr>
			<th align="center">Severity</th>
			<th align="center">Time</th>
			<th align="center">Module</th>
			<th align="center">Message</th>
		</tr>
	<xsl:for-each select="Message" >
	<!-- TODO: Add class for row -->
		<tr>
			<xsl:choose>
			  <xsl:when test="@Severity='WARNING'">
			   <xsl:attribute name="class">WarningRow </xsl:attribute>
			   <td align="center" width="25px"><img src=".\Resources\WarningHS.png" width="16" height="16"/></td>
			  </xsl:when>
			  <xsl:when test="@Severity='ERROR'">
			  <xsl:attribute name="class">ErrorRow </xsl:attribute>
			   <td align="center" width="25px"><img src=".\Resources\eventlogError.ico" width="16" height="16"/></td>
			  </xsl:when>
			  <xsl:otherwise >
			  <xsl:attribute name="class">MessageRow </xsl:attribute>
			   <td align="center" width="25px"><img src=".\Resources\eventlogInfo.ico" width="16" height="16"/></td>
			  </xsl:otherwise >
			</xsl:choose>
			<td width="100px"><xsl:value-of select="@TimeStamp" /></td>
			<td><xsl:value-of select="@Origin" /></td>
			<td><xsl:value-of select="." /></td>
		</tr>
	</xsl:for-each>
	</table>
</xsl:template>
</xsl:stylesheet>