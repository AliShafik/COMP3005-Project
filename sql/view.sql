
-- view: available fitness classes
CREATE VIEW view_available_classes AS
SELECT
    class_id,
    trainer_id,
    booking_id,
    class_name,
    capacity,
    num_signed_up
FROM "FitnessClass";
