from email.policy import default
from sqlalchemy import Boolean, Column, String, DateTime, BIGINT, Text
from .wpdb import Base

class Wmap(Base):
    __tablename__ = "wmap"
    
    id = Column(BIGINT, primary_key=True, index=True, nullable=False)
    site = Column(String(255), unique=True)
    redirection = Column(Text)
    ip = Column(String(255))
    hosting_provider = Column(String(255))
    wp_version = Column(Text)
    first_seen = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)

class Cycognito(Base):
    __tablename__ = "cycognito"
    
    id = Column(BIGINT, primary_key=True, index=True, nullable=False)
    site = Column(String(255), unique=True)
    ip = Column(String(255))
    hosting_provider = Column(String(255))
    first_seen = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)
    
class Amass(Base):
    __tablename__ = "amass"

    id = Column(BIGINT, primary_key=True, index=True, nullable=False)
    site = Column(String(255), unique=True)
    first_seen = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)
    
class Terminus(Base):
    __tablename__ = "terminus"

    id = Column(BIGINT, primary_key=True, index=True, nullable=False)
    environment = Column(String(255))
    site = Column(String(255), unique=True)
    plugins = Column(BIGINT, nullable=True)
    first_seen = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)
    
class TerminusPlugins(Base):
    __tablename__ = "terminus_plugins"

    id = Column(BIGINT, primary_key=True, index=True, nullable=False)
    environment = Column(String(255))
    site = Column(String(255))
    plugin = Column(String(255))
    _version_ = Column(String(255))
    status = Column(String(255))
    _update_ = Column(String(255))
    first_seen = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)
    
class Wpscan(Base):
    __tablename__ = 'wpscan_sites'
    
    id = Column(BIGINT, primary_key=True, index=True, nullable=False)
    source = Column(String(255), nullable=False)
    environment = Column(String(255))
    site = Column(String(255), unique=True)
    redirection = Column(Text)
    ip = Column(String(255))
    wp_version = Column(Text)
    wp_vulns = Column(BIGINT, nullable=True, default=0)
    plugins = Column(BIGINT, nullable=True)
    plugin_vulns = Column(BIGINT, nullable=True, default=0)
    first_seen = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)
    
class WpscanPlugins(Base):
    __tablename__ = 'wpscan_plugins'

    id = Column(BIGINT, primary_key=True, index=True, nullable=False)
    source = Column(String(255), nullable=False)
    environment = Column(String(255))
    site = Column(String(255))
    plugin = Column(String(255))
    location = Column(String(255))
    _version_ = Column(String(255))
    latest_version = Column(String(255))
    last_updated = Column(DateTime, nullable=True)
    outdated = Column(Boolean, default=True)
    first_seen = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)
    
class WPscanPluginVulns(Base):
    __tablename__ = 'wpscan_plugin_vulns'
    
    id = Column(BIGINT, primary_key=True, index=True, nullable=False)
    environment = Column(String(255))
    site = Column(String(255))
    plugin = Column(String(255))
    _version_ = Column(String(255))
    severity = Column(String(255))
    cve = Column(String(255))
    finding = Column(String(255))
    fixed_in = Column(String(255))
    reference = Column(String(255))
    first_seen = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)
    remediated = Column(Boolean, default=True)
    remediation_date = Column(DateTime, nullable=True)
    false_positive = Column(Boolean, default=True)
    owner = Column(String(255))
    notes = Column(String(255))
    
class WPscanPluginVulns(Base):
    __tablename__ = 'wpscan_vulns'
    
    id = Column(BIGINT, primary_key=True, index=True, nullable=False)
    site = Column(String(255))
    environment = Column(String(255))
    wp_version = Column(String(255))
    severity = Column(String(255))
    cve = Column(String(255))
    finding = Column(String(255))
    fixed_in = Column(String(255))
    reference = Column(String(255))
    first_seen = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)
    remediated = Column(Boolean, default=True)
    remediation_date = Column(DateTime, nullable=True)
    false_positive = Column(Boolean, default=True)
    owner = Column(String(255))
    notes = Column(String(255))

class WordpressSites(Base):
    __tablename__ = "wordpress_sites"
    
    id = Column(BIGINT, primary_key=True, index=True, nullable=False)
    environment = Column(String(255))
    site = Column(String(255), unique=True)
    redirection = Column(Text)
    ip = Column(String(255))
    hosting_provider = Column(String(255))
    owner = Column(String(255))
    wp_version = Column(Text)
    wp_vulns = Column(BIGINT, nullable=True)
    plugins = Column(BIGINT, nullable=True)
    plugin_vulns = Column(BIGINT, nullable=True)
    first_seen = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)
    valid_site = Column(Boolean, default=True)

class WordpressPlugins(Base):
    __tablename__ = "wordpress_plugins"
    
    id = Column(BIGINT, primary_key=True, index=True, nullable=False)
    environment = Column(String(255))
    site = Column(String(255))
    plugin = Column(String(255))
    location = Column(String(255))
    _version_ = Column(String(255))
    status = Column(String(255))
    latest_version = Column(String(255))
    last_updated = Column(DateTime, nullable=True)
    _update_ = Column(String(255))
    outdated = Column(Boolean)
    first_seen = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)
    
class Redirects(Base):
    __tablename__ = "redirects"
    
    id = Column(BIGINT, primary_key=True, index=True, nullable=False)
    site = Column(String(255))
    redirection = Column(Text)
    first_seen = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)