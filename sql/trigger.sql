
-- trigger: prevent overlapping RoomBooking for same room
-- function for trigger

CREATE OR REPLACE FUNCTION prevent_roombooking_overlap() RETURNS trigger AS $$
BEGIN
    IF EXISTS (
    SELECT 1 FROM "RoomBooking"
    WHERE room_id = NEW.room_id
        AND is_booked = TRUE
        AND start_time < NEW.end_time
        AND end_time > NEW.start_time
        AND (TG_OP = 'INSERT' OR (TG_OP = 'UPDATE' AND booking_id <> NEW.booking_id))
    ) THEN
    RAISE EXCEPTION 'Room booking overlaps existing booking';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- create trigger only if not exists

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trg_prevent_roombooking_overlap') THEN
    CREATE TRIGGER trg_prevent_roombooking_overlap
    BEFORE INSERT OR UPDATE ON "RoomBooking"
    FOR EACH ROW EXECUTE FUNCTION prevent_roombooking_overlap();
    END IF;
END;
$$;