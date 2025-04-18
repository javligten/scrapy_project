from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Property table
class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True)
    price = Column(Float)
    rental_status = Column(String)
    num_rooms = Column(Integer)
    num_bedrooms = Column(Integer)
    property_type = Column(String)
    surface_area = Column(Float)

    # Relationship with PropertyImage table
    images = relationship("PropertyImage", back_populates="property", cascade="all, delete-orphan")

    # Relationship with PropertyFeatureValue table
    feature_values = relationship("PropertyFeatureValue", back_populates="property", cascade="all, delete-orphan")

    # Linking Agent table with ForeignKey
    agent_id = Column(Integer, ForeignKey('agents.id'))
    agent = relationship("Agent", back_populates="properties")


# Feature Table
class Feature(Base):
    __tablename__ = 'features'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)


# PropertyFeatureValue Table
class PropertyFeatureValue(Base):
    __tablename__ = 'property_feature_values'

    id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey('properties.id'), nullable=False)
    feature_id = Column(Integer, ForeignKey('features.id'), nullable=False)
    feature_value = Column(String)

    # Relationships
    property = relationship("Property", back_populates="feature_values")
    feature = relationship("Feature")


# Agent Table
class Agent(Base):
    __tablename__ = 'agents'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String)

    # Relationship to Property table
    properties = relationship("Property", back_populates="agent")


# PropertyImage Table
class PropertyImage(Base):
    __tablename__ = 'property_images'
    
    id = Column(Integer, primary_key=True)
    url = Column(String)
    property_id = Column(Integer, ForeignKey('properties.id'))
    
    # Relationship to Property table
    property = relationship("Property", back_populates="images")
