class BoardProcessingRequest < ActiveRecord::Base
  serialize :request_params, JSON
  serialize :strategy, JSON
  serialize :board, Board
  serialize :result, JSON

  validates_presence_of :board, :strategy
  validates_presence_of :result, if: :completed?
  validate :datetimes_make_sense

  def succeeded?
    status == 'success'
  end

  def partially_succeeded?
    status == 'partial_success'
  end

  def failed?
    ['error', 'fatal_error'].include? status
  end

  def completed?
    not completed_at.blank?
  end

  def started?
    not started_at.blank?
  end

  def submitted?
    not submitted_at.blank?
  end

  def submit!
    raise "Can't submit a request that wasn't persisted yet" unless persisted?
    raise "Request was already submitted" if submitted?

    logger.debug "submitting BoardProcessingRequest[#{id}]"
    update_attributes! submitted_at: Time.now

    jid = GriddlersSolverWorker.perform_async(id)

    sidekiq_jid = jid
    save!
  end


  protected
  def datetimes_make_sense
    if submitted?
      unless started?
        errors.add :completed_at, "can't be set when started_at is nil" if completed?
      end
    else
      errors.add :completed_at, "can't be set when submitted_at is nil" if completed?
      errors.add :started_at, "can't be set when submitted_at is nil" if started?
    end
  end
end
