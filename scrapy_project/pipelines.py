from db.models import Property, PropertyFeatureValue, PropertyImage, Agent, Feature, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from scrapy import Spider
from scrapy_project.items import PropertyItem
import logging

class PostgresPipeline:
    def __init__(self) -> None:
        """Start database connection."""
        self.engine = create_engine('postgresql://postgres:password@db:5432/scrapy_db')
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def process_item(self, item: PropertyItem, spider: Spider) -> PropertyItem:
        """Store processed item into database."""
        session = self.Session()
        try:
            property = Property(
                price=item['price'],
                rental_status=item['rental_status'],
                num_rooms=item['num_rooms'],
                num_bedrooms=item['num_bedrooms'],
                property_type=item['property_type'],
                surface_area=item['surface_area'],
            )
            
            # Add property for features
            session.add(property)
            session.commit()
            
            # Process additional features
            for feature_name, feature_value in item['features'].items():
                if feature_value.strip():  # Ignore empty values
                    # Check for existing features
                    feature = session.query(Feature).filter_by(name=feature_name).first()
                    if not feature:
                        # Create feature if it doesn't exist
                        feature = Feature(name=feature_name)
                        session.add(feature)
                        session.commit()

                    # Add FeatureValue to PropertyFeatureValue
                    property_feature_value = PropertyFeatureValue(
                        property_id=property.id,
                        feature_id=feature.id,
                        feature_value=feature_value
                    )
                    session.add(property_feature_value)
            
            # Process image(s)
            if item.get('image_urls'):
                for url in item.get('image_urls', []):
                    image = PropertyImage(url=url, property_id=property.id)
                    session.add(image)
            
            # Process agent information
            if item.get('agent_name'):
                # Check if agent already exists
                agent = session.query(Agent).filter_by(name=item['agent_name']).first()
                if not agent:
                    agent = Agent(
                        name=item['agent_name'],
                        phone=item.get('agent_phone', ''),
                        email=item.get('agent_email', '')
                    )
                    session.add(agent)
                    session.commit()
                    
                # Assign agent to property
                property.agent = agent
            
            # Commit all changes
            session.commit()
            
        except IntegrityError as e:
            session.rollback()
            logging.error(f"Integrity error while processing item: {e}")
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"SQLAlchemy error while processing item: {e}")
        except Exception as e:
            session.rollback()
            logging.error(f"Unexpected error: {e}")
        finally:
            session.close()
        
        return item
