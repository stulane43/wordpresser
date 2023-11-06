from sqlalchemy import Boolean, Column, String, DateTime, BIGINT, Text
from .wpdb import Base

class WordpressSites(Base):
    __tablename__ = "wordpress_sites"
    
    id = Column(BIGINT, primary_key=True, index=True, nullable=False)
    site = Column(String(255), unique=True)
    target = Column(Text, nullable=True)
    wp_version = Column(Text, nullable=True)
    plugins = Column(BIGINT, nullable=True)
    plugin_vulns = Column(BIGINT, nullable=True)
    first_seen = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)
    owner = Column(String(255), nullable=True)
    valid_site = Column(Boolean, default=True)
    
class WordpressPlugins(Base):
    __tablename__ = "wordpress_plugins"
    
    id = Column(BIGINT, primary_key=True, index=True, nullable=False)
    target = Column(String(255))
    plugin = Column(String(255))
    plugin_version = Column(String(255), nullable=True)
    vulnerable = Column(Boolean, nullable=True)
    first_seen = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)
    plugin_status = Column(String(255), default='Active')
      
class WPscanPluginVulns(Base):
    __tablename__ = 'wordpress_plugin_vulns'
    
    id = Column(BIGINT, primary_key=True, index=True, nullable=False)
    target = Column(String(255))
    plugin = Column(String(255))
    version_affected = Column(String(255), nullable=True)
    version_fixed = Column(String(255), nullable=True)
    vulnerability = Column(String(255), nullable=True)
    reference = Column(String(255), nullable=True)
    triage_status = Column(String(255), default='To Verify')
    remediation_status = Column(String(255), default='New')
    remediated = Column(Boolean, default=False)
    remediation_date = Column(DateTime, nullable=True)
    first_seen = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)
    false_positive = Column(Boolean, default=False)
    owner = Column(String(255), nullable=True)
    owner_notes = Column(String(255), nullable=True)
    security_notes = Column(String(255), nullable=True)
    ManuallyRemediated = Column(Boolean, nullable=False, default=False)
