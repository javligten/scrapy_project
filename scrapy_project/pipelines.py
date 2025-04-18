from db.models import Property, PropertyFeatureValue, PropertyImage, Agent, Feature, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import logging

class PostgresPipeline:
    def __init__(self):
        self.engine = create_engine('postgresql://postgres:password@db:5432/scrapy_db')
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
        
    def process_item(self, item, spider):
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
            
            # Add property before features
            session.add(property)
            session.commit()  # To use property.id for references
            
            # Handling features
            for feature_name, feature_value in item['features'].items():
                if feature_value.strip():  # Ignore empty values
                    # Check if feature already exists
                    feature = session.query(Feature).filter_by(name=feature_name).first()
                    if not feature:
                        # If feature doesn't exist, create it
                        feature = Feature(name=feature_name)
                        session.add(feature)
                        session.commit()  # Commit to get feature.id

                    # Add feature's value to PropertyFeatureValue
                    property_feature_value = PropertyFeatureValue(
                        property_id=property.id,
                        feature_id=feature.id,
                        feature_value=feature_value
                    )
                    session.add(property_feature_value)
            
            # Handling image URLs
            if item.get('image_urls'):
                for url in item.get('image_urls', []):
                    image = PropertyImage(url=url, property_id=property.id)
                    session.add(image)
            
            # Handling agent information
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
                    session.commit()  # Commit to get agent.id
                    
                # Assign agent to property
                property.agent = agent
            
            # Commit changes to session
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
